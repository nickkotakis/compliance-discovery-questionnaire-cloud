"""Flask REST API server for compliance discovery questionnaire."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import Dict, Any, List
from datetime import datetime
import json
import os

from compliance_discovery.nist_parser import NIST80053Parser
from compliance_discovery.question_generator import DiscoveryQuestionGenerator
from compliance_discovery.mcp_integration import MCPClient, create_aws_hints
from compliance_discovery.models.control import Control
from compliance_discovery.models.question import DiscoveryQuestion
from compliance_discovery.database import db, SessionModel
from compliance_discovery.control_descriptions import get_control_description
from compliance_discovery.aws_control_mapping import get_aws_responsibility, get_aws_services


app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "sessions.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables on startup (moved to main block to avoid double initialization)
# with app.app_context():
#     db.create_all()

# Global state
controls_cache: List[Control] = []
questions_cache: Dict[str, List[DiscoveryQuestion]] = {}
mcp_data_cache: Dict[str, List[Dict[str, Any]]] = {}  # Cache for MCP data from JSON file

# Initialize components
parser = NIST80053Parser()
generator = DiscoveryQuestionGenerator()
mcp_client = MCPClient()


def load_mcp_data():
    """Load AWS controls data from MCP JSON file."""
    global mcp_data_cache
    
    mcp_file = os.path.join(basedir, 'aws_controls_mcp_data.json')
    if os.path.exists(mcp_file):
        try:
            with open(mcp_file, 'r') as f:
                data = json.load(f)
                mcp_data_cache = data.get('controls', {})
                print(f"Loaded MCP data for {len(mcp_data_cache)} controls from {mcp_file}")
        except Exception as e:
            print(f"Warning: Could not load MCP data file: {str(e)}")
            mcp_data_cache = {}
    else:
        print(f"Note: MCP data file not found at {mcp_file}")
        mcp_data_cache = {}


def initialize_data():
    """Initialize controls and questions data."""
    global controls_cache, questions_cache
    
    if not controls_cache:
        print("Loading NIST 800-53 Moderate Baseline controls...")
        controls_cache = parser.get_moderate_baseline_controls()
        print(f"Loaded {len(controls_cache)} controls")
        print(f"Sample control IDs: {[c.id for c in controls_cache[:10]]}")
        
        print("Generating discovery questions...")
        for control in controls_cache:
            questions = generator.generate_questions(control)
            questions_cache[control.id] = questions
        print(f"Generated questions for {len(questions_cache)} controls")
        
        # Load MCP data
        load_mcp_data()


@app.after_request
def after_request(response):
    """Add CORS headers to all responses."""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response


@app.route('/api/controls', methods=['OPTIONS'])
@app.route('/api/controls/<control_id>', methods=['OPTIONS'])
@app.route('/api/questions', methods=['OPTIONS'])
@app.route('/api/session', methods=['OPTIONS'])
@app.route('/api/session/<session_id>', methods=['OPTIONS'])
@app.route('/api/session/<session_id>/response', methods=['OPTIONS'])
@app.route('/api/sessions', methods=['OPTIONS'])
@app.route('/api/export', methods=['OPTIONS'])
def handle_options(control_id=None, session_id=None):
    """Handle OPTIONS preflight requests."""
    return '', 204


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/controls', methods=['GET'])
def get_controls():
    """Get all Moderate Baseline controls.
    
    Query parameters:
        family: Filter by control family (optional)
    """
    initialize_data()
    
    family = request.args.get('family')
    
    filtered_controls = controls_cache
    if family:
        filtered_controls = [c for c in controls_cache if c.family.upper() == family.upper()]
    
    # Sort controls alphabetically by ID with natural number sorting
    def sort_key(control):
        # Split ID into parts (e.g., "AC-11" -> ["AC", 11])
        parts = control.id.upper().split('-')
        if len(parts) == 2:
            family_code = parts[0]
            try:
                # Handle enhancements like AC-11(1)
                if '(' in parts[1]:
                    base_num = int(parts[1].split('(')[0])
                    enh_num = int(parts[1].split('(')[1].rstrip(')'))
                    return (family_code, base_num, enh_num)
                else:
                    return (family_code, int(parts[1]), 0)
            except ValueError:
                return (family_code, 0, 0)
        return (control.id.upper(), 0, 0)
    
    sorted_controls = sorted(filtered_controls, key=sort_key)
    
    return jsonify({
        'controls': [
            {
                'id': c.id,
                'title': c.title,
                'description': get_control_description(c.id) or c.description,
                'family': c.family,
                'in_moderate_baseline': c.in_moderate_baseline,
                'parameter_count': len(c.parameters),
                'enhancement_count': len(c.enhancements)
            }
            for c in sorted_controls
        ],
        'total': len(sorted_controls)
    })


@app.route('/api/controls/<control_id>', methods=['GET'])
def get_control(control_id: str):
    """Get specific control with questions and AWS mappings.
    
    Args:
        control_id: NIST control ID (e.g., "AC-1" or "ac-1")
    """
    initialize_data()
    
    # Normalize control ID to uppercase for comparison
    normalized_id = control_id.upper()
    
    # Find control (case-insensitive)
    control = next((c for c in controls_cache if c.id.upper() == normalized_id), None)
    if not control:
        print(f"Control not found: {control_id} (normalized: {normalized_id})")
        print(f"Available controls: {[c.id for c in controls_cache[:5]]}")
        return jsonify({'error': f'Control not found: {control_id}'}), 404
    
    # Get questions (use actual control ID from cache)
    questions = questions_cache.get(control.id, [])
    
    # Try to get AWS mappings using normalized ID
    aws_hints = []
    aws_controls_data = []  # Store full control data for detailed view
    
    # First try loading from MCP data cache (JSON file)
    if normalized_id.lower() in mcp_data_cache:
        aws_controls_data = mcp_data_cache[normalized_id.lower()]
        print(f"Loaded {len(aws_controls_data)} AWS controls for {normalized_id} from MCP cache")
        # Generate hints from cached data
        if aws_controls_data:
            for ac in aws_controls_data:
                hint_parts = []
                if ac.get('services'):
                    services = ", ".join(ac['services'][:2])
                    hint_parts.append(f"Services: {services}")
                if ac.get('config_rules'):
                    rules = ", ".join(ac['config_rules'][:2])
                    hint_parts.append(f"Config: {rules}")
                if ac.get('security_hub_controls'):
                    hub = ", ".join(ac['security_hub_controls'][:2])
                    hint_parts.append(f"Security Hub: {hub}")
                if hint_parts:
                    aws_hints.append(f"• {ac['title']}\n  {' | '.join(hint_parts)}")
    
    # Fallback: Try MCP server (if available)
    if not aws_controls_data:
        try:
            if mcp_client.connected or mcp_client.connect():
                aws_controls = mcp_client.map_compliance_requirements(normalized_id)
                if aws_controls:
                    aws_hints = create_aws_hints(aws_controls)
                    # Store detailed control data
                    aws_controls_data = [
                        {
                            'control_id': ac.control_id,
                            'title': ac.title,
                            'description': ac.description,
                            'services': ac.services,
                            'config_rules': ac.managed_controls.config_rules,
                            'security_hub_controls': ac.managed_controls.security_hub_controls,
                            'control_tower_ids': ac.managed_controls.control_tower_ids,
                            'frameworks': ac.frameworks
                        }
                        for ac in aws_controls
                    ]
        except Exception as e:
            print(f"Warning: Could not fetch AWS mappings from MCP: {str(e)}")
    
    # Final fallback to manual mapping if nothing else worked
    if not aws_hints:
        fallback_services = get_aws_services(control.id)
        if fallback_services:
            aws_hints = [f"AWS Services: {', '.join(fallback_services)}"]
    
    # Determine responsibility using fallback mapping
    responsibility = get_aws_responsibility(control.id)
    
    # Build applicability message based on responsibility
    if responsibility == 'aws':
        aws_applicability = {
            'applicable': False,
            'responsibility': 'aws',
            'message': '🟠 AWS RESPONSIBILITY: AWS handles this control for their infrastructure. Your AWS workloads automatically inherit this protection. Download compliance reports from AWS Artifact to demonstrate this to auditors.',
            'artifact_links': [
                {
                    'name': 'AWS Artifact (Compliance Reports)',
                    'url': 'https://console.aws.amazon.com/artifact/',
                    'description': 'Download reports showing AWS implementation of this control'
                },
                {
                    'name': 'AWS Data Center Security',
                    'url': 'https://aws.amazon.com/compliance/data-center/',
                    'description': 'Learn about AWS physical security measures'
                }
            ],
            'controls': []
        }
    elif responsibility == 'shared' and aws_hints:
        aws_applicability = {
            'applicable': True,
            'responsibility': 'shared',
            'message': f'🟢 SHARED RESPONSIBILITY: AWS provides the services listed below. You must configure and use them properly in your AWS environment to meet this requirement.',
            'artifact_links': [
                {
                    'name': 'AWS Artifact (Compliance Reports)',
                    'url': 'https://console.aws.amazon.com/artifact/',
                    'description': 'Download SOC, PCI, ISO reports showing AWS platform compliance'
                },
                {
                    'name': 'AWS Compliance Programs',
                    'url': 'https://aws.amazon.com/compliance/programs/',
                    'description': 'View AWS compliance certifications'
                }
            ],
            'controls': aws_hints
        }
    else:
        aws_applicability = {
            'applicable': False,
            'responsibility': 'customer',
            'message': '🔵 CUSTOMER RESPONSIBILITY: You must implement this control in your AWS environment using custom configurations, third-party tools, or application-level controls.',
            'artifact_links': [],
            'controls': []
        }
    
    # Clean the description for display - use human-friendly version if available
    human_description = get_control_description(control.id)
    cleaned_description = human_description if human_description else control.description
    
    return jsonify({
        'control': {
            'id': control.id,
            'title': control.title,
            'description': cleaned_description,
            'family': control.family,
            'in_moderate_baseline': control.in_moderate_baseline,
            'parameters': [
                {
                    'id': p.id,
                    'label': p.label,
                    'description': p.description,
                    'constraints': p.constraints
                }
                for p in control.parameters
            ],
            'enhancements': [
                {
                    'id': e.id,
                    'title': e.title,
                    'description': e.description,
                    'in_moderate_baseline': e.in_moderate_baseline
                }
                for e in control.enhancements
            ]
        },
        'questions': [
            {
                'id': q.id,
                'control_id': q.control_id,
                'question_text': q.question_text,
                'question_type': q.question_type.value,
                'family': q.family,
                'aws_service_guidance': q.aws_service_guidance
            }
            for q in questions
        ],
        'aws_hints': aws_hints,
        'aws_applicability': aws_applicability,
        'aws_controls': aws_controls_data  # Add detailed AWS control data
    })


@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Get all questions.
    
    Query parameters:
        control_id: Filter by control ID (optional)
        family: Filter by family (optional)
        question_type: Filter by question type (optional)
    """
    initialize_data()
    
    control_id = request.args.get('control_id')
    family = request.args.get('family')
    question_type = request.args.get('question_type')
    
    all_questions = []
    for questions in questions_cache.values():
        all_questions.extend(questions)
    
    # Apply filters
    if control_id:
        all_questions = [q for q in all_questions if q.control_id == control_id]
    if family:
        all_questions = [q for q in all_questions if q.family == family]
    if question_type:
        all_questions = [q for q in all_questions if q.question_type.value == question_type]
    
    return jsonify({
        'questions': [
            {
                'id': q.id,
                'control_id': q.control_id,
                'question_text': q.question_text,
                'question_type': q.question_type.value,
                'family': q.family,
                'aws_service_guidance': q.aws_service_guidance
            }
            for q in all_questions
        ],
        'total': len(all_questions)
    })


@app.route('/api/session', methods=['POST'])
def create_session():
    """Create new assessment session.
    
    Request body:
        {
            "customer_name": str,
            "analyst_name": str,
            "frameworks": List[str]
        }
    """
    data = request.get_json()
    
    session_id = f"session-{datetime.utcnow().timestamp()}"
    
    session_data = {
        'id': session_id,
        'customer_name': data.get('customer_name', ''),
        'analyst_name': data.get('analyst_name', ''),
        'frameworks': data.get('frameworks', ['NIST 800-53']),
        'status': 'active',
        'responses': {},
        'evidence': {}
    }
    
    # Save to database
    session_model = SessionModel.from_dict(session_data)
    db.session.add(session_model)
    db.session.commit()
    
    return jsonify(session_model.to_dict()), 201


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id: str):
    """Get session details."""
    session = SessionModel.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify(session.to_dict())


@app.route('/api/session/<session_id>/response', methods=['POST'])
def record_response(session_id: str):
    """Record a response to a question.
    
    Request body:
        {
            "question_id": str,
            "answer": str,
            "notes": str (optional)
        }
    """
    session = SessionModel.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    data = request.get_json()
    question_id = data.get('question_id')
    
    # Update responses
    responses = json.loads(session.responses) if session.responses else {}
    responses[question_id] = {
        'answer': data.get('answer', ''),
        'notes': data.get('notes', ''),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    session.responses = json.dumps(responses)
    session.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True})


@app.route('/api/export', methods=['GET'])
def export_template():
    """Export blank template.
    
    Query parameters:
        format: Export format (json, csv, excel) - default: json
    """
    initialize_data()
    
    export_format = request.args.get('format', 'json')
    
    template_data = {
        'metadata': {
            'template_version': '1.0.0',
            'baseline_version': 'NIST 800-53 Rev 5 Moderate Baseline',
            'export_date': datetime.utcnow().isoformat(),
            'total_control_count': len(controls_cache),
            'frameworks_included': ['NIST 800-53', 'AWS']
        },
        'controls': [
            {
                'id': c.id,
                'title': c.title,
                'description': c.description,
                'family': c.family
            }
            for c in controls_cache
        ],
        'questions': {
            control_id: [
                {
                    'id': q.id,
                    'question_text': q.question_text,
                    'question_type': q.question_type.value,
                    'response': ''
                }
                for q in questions
            ]
            for control_id, questions in questions_cache.items()
        }
    }
    
    if export_format == 'json':
        return jsonify(template_data)
    else:
        return jsonify({'error': 'Only JSON format supported in this version'}), 400


@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List all sessions."""
    sessions = SessionModel.query.order_by(SessionModel.created_at.desc()).all()
    return jsonify({
        'sessions': [s.to_dict() for s in sessions],
        'total': len(sessions)
    })


if __name__ == '__main__':
    print("Starting Compliance Discovery API Server...")
    print("Initializing database...")
    with app.app_context():
        db.create_all()
    print("Initializing data...")
    initialize_data()
    print("Server ready!")
    app.run(debug=True, port=5001)
