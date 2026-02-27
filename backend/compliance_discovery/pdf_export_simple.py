"""
Simple PDF export using fpdf2 (pure Python, no C extensions)
This avoids the Pillow/_imaging import issues on Lambda
"""
from fpdf import FPDF
from io import BytesIO


def sanitize_text(text):
    """
    Sanitize text for PDF export by replacing Unicode characters
    that aren't supported by standard fonts
    """
    if not text:
        return text
    
    # Replace common Unicode characters with ASCII equivalents
    replacements = {
        '\u2019': "'",  # Right single quotation mark
        '\u2018': "'",  # Left single quotation mark
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2013': '-',  # En dash
        '\u2014': '--', # Em dash
        '\u2022': '-',  # Bullet
        '\u2026': '...', # Ellipsis
        '\u00a0': ' ',  # Non-breaking space
    }
    
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    
    # Remove any remaining non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    return text


class CompliancePDF(FPDF):
    """Custom PDF class for compliance questionnaires"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """Page header"""
        self.set_font('Arial', 'B', 12)
        self.set_text_color(54, 96, 146)  # Primary blue
        self.cell(0, 10, sanitize_text('Compliance Discovery Questionnaire'), 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        """Page footer"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title, level=1):
        """Add a chapter/section title"""
        title = sanitize_text(title)
        if level == 1:
            self.set_font('Arial', 'B', 14)
            self.set_fill_color(54, 96, 146)  # Primary blue
            self.set_text_color(255, 255, 255)  # White text
            self.cell(0, 10, title, 0, 1, 'L', 1)
        elif level == 2:
            self.set_font('Arial', 'B', 12)
            self.set_fill_color(227, 242, 253)  # Light blue
            self.set_text_color(54, 96, 146)  # Primary blue
            self.cell(0, 8, title, 0, 1, 'L', 1)
        else:
            self.set_font('Arial', 'B', 10)
            self.set_text_color(0, 0, 0)
            self.cell(0, 6, title, 0, 1, 'L')
        self.ln(2)
        
    def add_text(self, text, bold=False, indent=0):
        """Add text with optional bold and indent"""
        text = sanitize_text(text)
        self.set_font('Arial', 'B' if bold else '', 10)
        self.set_text_color(0, 0, 0)
        self.set_x(10 + indent)
        self.multi_cell(0, 5, text)
        
    def add_colored_box(self, text, bg_color, text_color=(0, 0, 0)):
        """Add text in a colored box"""
        text = sanitize_text(text)
        self.set_fill_color(*bg_color)
        self.set_text_color(*text_color)
        self.set_font('Arial', '', 9)
        self.multi_cell(0, 6, text, 0, 'L', 1)
        self.ln(2)
        
    def add_response_field(self, label, height=20):
        """Add a response field box"""
        label = sanitize_text(label)
        self.set_font('Arial', 'B', 9)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, label, 0, 1)
        
        # Draw response box
        self.set_fill_color(255, 250, 205)  # Light yellow
        self.set_draw_color(200, 200, 200)  # Gray border
        x = self.get_x()
        y = self.get_y()
        self.rect(x, y, 190, height, 'D')
        self.ln(height + 2)


def generate_simple_pdf(template_data):
    """
    Generate a simple PDF questionnaire
    
    Args:
        template_data: Dictionary with questionnaire data
        
    Returns:
        bytes: PDF file content
    """
    pdf = CompliancePDF()
    pdf.add_page()
    
    # Title page
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(54, 96, 146)
    pdf.cell(0, 20, sanitize_text('Compliance Discovery'), 0, 1, 'C')
    pdf.cell(0, 15, sanitize_text('Questionnaire'), 0, 1, 'C')
    pdf.ln(10)
    
    # Subtitle
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(90, 127, 163)
    pdf.cell(0, 10, sanitize_text('NIST 800-53 Rev 5 Moderate Baseline'), 0, 1, 'C')
    pdf.ln(15)
    
    # Metadata
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    metadata = template_data.get('metadata', {})
    
    pdf.cell(50, 8, sanitize_text('Export Date:'), 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, sanitize_text(str(metadata.get('export_date', 'N/A'))), 0, 1)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 8, sanitize_text('Total Controls:'), 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, str(metadata.get('total_control_count', 0)), 0, 1)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 8, sanitize_text('Frameworks:'), 0, 0)
    pdf.set_font('Arial', '', 10)
    frameworks = ', '.join(metadata.get('frameworks_included', []))
    pdf.multi_cell(0, 8, sanitize_text(frameworks))
    
    pdf.ln(10)
    
    # Instructions
    pdf.add_colored_box(
        'Instructions:\n'
        '- This questionnaire assesses compliance with NIST 800-53 Rev 5 Moderate Baseline\n'
        '- Questions are organized by control family and type\n'
        '- Fill in response fields with detailed answers and specific examples\n'
        '- Document evidence locations and attach supporting materials',
        (255, 250, 205)  # Light yellow
    )
    
    # Controls
    pdf.add_page()
    
    # Sort controls by family
    controls = template_data.get('controls', [])
    questions_map = template_data.get('questions', {})
    
    def sort_key(control):
        parts = control['id'].upper().split('-')
        if len(parts) == 2:
            family_code = parts[0]
            try:
                if '(' in parts[1]:
                    base_num = int(parts[1].split('(')[0])
                    enh_num = int(parts[1].split('(')[1].rstrip(')'))
                    return (family_code, base_num, enh_num)
                else:
                    return (family_code, int(parts[1]), 0)
            except ValueError:
                return (family_code, 0, 0)
        return (control['id'].upper(), 0, 0)
    
    sorted_controls = sorted(controls, key=sort_key)
    
    # Family names
    family_names = {
        'ac': 'Access Control', 'at': 'Awareness and Training',
        'au': 'Audit and Accountability', 'ca': 'Assessment, Authorization, and Monitoring',
        'cm': 'Configuration Management', 'cp': 'Contingency Planning',
        'ia': 'Identification and Authentication', 'ir': 'Incident Response',
        'ma': 'Maintenance', 'mp': 'Media Protection',
        'pe': 'Physical and Environmental Protection', 'pl': 'Planning',
        'pm': 'Program Management', 'ps': 'Personnel Security',
        'pt': 'PII Processing and Transparency', 'ra': 'Risk Assessment',
        'sa': 'System and Services Acquisition', 'sc': 'System and Communications Protection',
        'si': 'System and Information Integrity', 'sr': 'Supply Chain Risk Management'
    }
    
    current_family = None
    control_count = 0
    
    for control in sorted_controls:
        family = control['family'].lower()
        
        # Add family header when family changes
        if current_family != family:
            if control_count > 0:
                pdf.add_page()
            current_family = family
            family_full_name = family_names.get(family, family.upper())
            pdf.chapter_title(f"{family.upper()} - {family_full_name}", level=1)
        
        control_count += 1
        
        # Control header
        responsibility = control.get('aws_responsibility', 'UNKNOWN').upper()
        pdf.chapter_title(
            f"{control['id'].upper()}: {control['title']} [AWS: {responsibility}]",
            level=2
        )
        
        # Control description
        pdf.add_colored_box(control['description'], (250, 250, 250))
        
        # Questions
        if control['id'] in questions_map:
            questions = questions_map[control['id']]
            
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(90, 127, 163)
            pdf.cell(0, 8, 'Assessment Questions', 0, 1)
            pdf.ln(2)
            
            for idx, q in enumerate(questions, 1):
                q_type = q['question_type'].upper()
                
                # Question
                pdf.set_font('Arial', 'B', 9)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(30, 6, f"[{q_type}]", 0, 0)
                pdf.set_font('Arial', '', 9)
                pdf.multi_cell(0, 6, sanitize_text(f"{idx}. {q['question_text']}"))
                
                # Response field
                pdf.add_response_field('RESPONSE:', 15)
                pdf.ln(2)
        
        # Evidence section
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(139, 157, 195)
        pdf.cell(0, 8, 'Evidence Documentation', 0, 1)
        
        pdf.add_response_field('Description:', 12)
        pdf.add_response_field('Location:', 10)
        pdf.add_response_field('Notes:', 12)
        
        pdf.ln(5)
        
        # Page break every 2 controls
        if control_count % 2 == 0:
            pdf.add_page()
    
    # Generate PDF
    return pdf.output()
