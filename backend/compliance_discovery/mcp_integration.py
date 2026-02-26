"""Integration with compass-control-guides MCP server for AWS control mappings.

NOTE: This module is designed to work with the compass-control-guides-remote MCP server
through Kiro's MCP integration. When running outside of Kiro, the MCP calls will fail
gracefully and fall back to the manual mappings in aws_control_mapping.py.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
from compliance_discovery.exceptions import (
    MCPConnectionError,
    MCPQueryError,
    MCPResponseError,
    AWSControlNotFoundError
)


@dataclass
class ManagedControls:
    """AWS managed control identifiers."""
    config_rules: List[str]
    security_hub_controls: List[str]
    control_tower_ids: List[str]


@dataclass
class AWSControl:
    """AWS Control Guide information."""
    control_id: str
    title: str
    description: str
    services: List[str]
    frameworks: List[str]
    managed_controls: ManagedControls
    nist_mappings: List[str]


class MCPClient:
    """Client for compass-control-guides MCP server.
    
    NOTE: This client is designed to work within Kiro's environment where MCP tools
    are available. When running standalone, it will gracefully fail and allow the
    application to fall back to manual AWS control mappings.
    """
    
    def __init__(self, server_name: str = "compass-control-guides-remote"):
        """Initialize MCP client.
        
        Args:
            server_name: Name of the MCP server in Kiro configuration
        """
        self.server_name = server_name
        self.connected = False
    
    def connect(self) -> bool:
        """Test connection to MCP server.
        
        Returns:
            True if connection successful
            
        Note:
            This always returns False when running outside Kiro environment.
            The application will fall back to manual mappings.
        """
        # MCP tools are only available within Kiro environment
        # When running standalone, gracefully fail and use fallback mappings
        print(f"Note: MCP server '{self.server_name}' not available in standalone mode.")
        print("Using fallback AWS control mappings from aws_control_mapping.py")
        self.connected = False
        return False
    
    def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool.
        
        NOTE: This method is not functional outside of Kiro environment.
        MCP tools are only available through Kiro's MCP integration.
        
        Args:
            tool_name: Name of the MCP tool to call
            arguments: Tool arguments
            
        Returns:
            Tool response as dictionary
            
        Raises:
            MCPQueryError: Always raises when called outside Kiro
        """
        raise MCPQueryError(
            "MCP tools are only available within Kiro environment. "
            "Use fallback mappings from aws_control_mapping.py instead."
        )
    
    def search_controls(self, query: str, limit: int = 10) -> List[AWSControl]:
        """Search AWS Control Guides using MCP.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of AWSControl objects matching the query
            
        Raises:
            MCPConnectionError: If MCP server is unavailable
            MCPQueryError: If MCP query fails
        """
        if not self.connected:
            if not self.connect():
                return []
        
        try:
            response = self._call_mcp_tool("search_controls", {
                "query": query,
                "limit": limit
            })
            
            return self._parse_controls(response.get("controls", []))
            
        except Exception as e:
            print(f"Warning: MCP search failed: {str(e)}")
            return []
    
    def get_control(self, control_id: str) -> Optional[AWSControl]:
        """Get detailed information about a specific AWS Control Guide.
        
        Args:
            control_id: AWS Control Guide ID (e.g., "AWS-CG-0000138")
            
        Returns:
            AWSControl object with full details or None if not found
        """
        if not self.connected:
            if not self.connect():
                return None
        
        try:
            response = self._call_mcp_tool("get_control", {
                "control_id": control_id
            })
            
            controls = self._parse_controls([response])
            return controls[0] if controls else None
            
        except Exception as e:
            print(f"Warning: MCP get_control failed: {str(e)}")
            return None
    
    def map_compliance_requirements(self, framework_control: str, framework: str = "NIST-SP-800-53-r5") -> List[AWSControl]:
        """Map framework control to AWS controls using MCP.
        
        This uses keyword-based search since MCP stores AWS Control Guides
        that reference NIST controls, not NIST control definitions.
        
        Args:
            framework_control: Framework control ID (e.g., "AC-2")
            framework: Framework name (default: "NIST-SP-800-53-r5")
            
        Returns:
            List of AWSControl objects that map to the framework control
        """
        if not self.connected:
            if not self.connect():
                return []
        
        try:
            # Map NIST control IDs to search keywords
            control_keywords = self._get_control_keywords(framework_control)
            
            # Search using keywords
            response = self._call_mcp_tool("search_controls", {
                "query": control_keywords,
                "limit": 20
            })
            
            # Filter results to only those that mention the framework
            results = response.get("results", [])
            filtered_results = [
                r for r in results 
                if framework in r.get("frameworks", [])
            ]
            
            return self._parse_controls(filtered_results)
            
        except Exception as e:
            print(f"Warning: MCP mapping failed: {str(e)}")
            return []
    
    def _get_control_keywords(self, control_id: str) -> str:
        """Map NIST control IDs to search keywords.
        
        Args:
            control_id: NIST control ID (e.g., "AC-2", "PE-4")
            
        Returns:
            Search keywords for the control
        """
        # Map common NIST controls to AWS service keywords
        keyword_map = {
            # Access Control
            'ac-1': 'access control policy',
            'ac-2': 'IAM user management account',
            'ac-3': 'IAM policy authorization',
            'ac-4': 'network security groups flow control',
            'ac-6': 'IAM least privilege',
            'ac-17': 'VPN remote access',
            
            # Audit and Accountability
            'au-1': 'audit logging policy',
            'au-2': 'CloudTrail logging events',
            'au-3': 'CloudTrail audit records',
            'au-4': 'CloudWatch log storage',
            'au-6': 'CloudWatch log analysis',
            'au-9': 'CloudTrail log protection',
            'au-11': 'S3 log retention',
            'au-12': 'CloudTrail audit generation',
            
            # Configuration Management
            'cm-1': 'configuration management policy',
            'cm-2': 'Config baseline configuration',
            'cm-3': 'Config change control',
            'cm-6': 'Config settings',
            'cm-7': 'security groups least functionality',
            'cm-8': 'Config inventory',
            
            # Contingency Planning
            'cp-1': 'contingency planning policy',
            'cp-6': 'alternate processing site',
            'cp-7': 'alternate processing site',
            'cp-9': 'backup EBS RDS S3',
            'cp-10': 'system recovery restore',
            
            # Identification and Authentication
            'ia-1': 'identification authentication policy',
            'ia-2': 'IAM authentication MFA',
            'ia-3': 'device identification',
            'ia-4': 'IAM identifier management',
            'ia-5': 'IAM password authenticator',
            'ia-8': 'IAM identification authentication',
            
            # Incident Response
            'ir-1': 'incident response policy',
            'ir-4': 'GuardDuty incident handling',
            'ir-5': 'incident monitoring',
            'ir-6': 'incident reporting',
            
            # Physical and Environmental Protection
            'pe-1': 'physical security policy',
            'pe-2': 'physical access authorization',
            'pe-3': 'physical access control',
            'pe-4': 'access control transmission',
            'pe-5': 'access control output devices',
            'pe-6': 'monitoring physical access',
            
            # System and Communications Protection
            'sc-1': 'system communications protection policy',
            'sc-7': 'security groups boundary protection',
            'sc-8': 'TLS transmission confidentiality',
            'sc-12': 'KMS cryptographic key',
            'sc-13': 'KMS cryptographic protection',
            'sc-28': 'EBS S3 RDS encryption',
            
            # System and Information Integrity
            'si-1': 'system information integrity policy',
            'si-2': 'Systems Manager patch flaw remediation',
            'si-3': 'GuardDuty malicious code protection',
            'si-4': 'GuardDuty monitoring',
            'si-7': 'integrity verification',
            
            # Risk Assessment
            'ra-1': 'risk assessment policy',
            'ra-5': 'Inspector vulnerability scanning',
        }
        
        # Get keywords or use control ID as fallback
        control_lower = control_id.lower()
        return keyword_map.get(control_lower, control_id)
    
    def _parse_controls(self, controls_data: List[Dict[str, Any]]) -> List[AWSControl]:
        """Parse control data from MCP response.
        
        Args:
            controls_data: List of control dictionaries from MCP
            
        Returns:
            List of AWSControl objects
        """
        controls = []
        
        for data in controls_data:
            try:
                managed = data.get("managed_controls", {})
                
                control = AWSControl(
                    control_id=data.get("control_id", ""),
                    title=data.get("title", ""),
                    description=data.get("description", ""),
                    services=data.get("services", []),
                    frameworks=data.get("frameworks", []),
                    managed_controls=ManagedControls(
                        config_rules=managed.get("config_rules", []),
                        security_hub_controls=managed.get("security_hub_controls", []),
                        control_tower_ids=managed.get("control_tower_ids", [])
                    ),
                    nist_mappings=data.get("nist_mappings", [])
                )
                controls.append(control)
            except Exception as e:
                print(f"Warning: Failed to parse control: {str(e)}")
                continue
        
        return controls
    
    def disconnect(self) -> None:
        """Disconnect from MCP server."""
        self.connected = False


def create_aws_hints(aws_controls: List[AWSControl]) -> List[str]:
    """Create detailed AWS hint strings from AWS controls.
    
    Args:
        aws_controls: List of AWS controls
        
    Returns:
        List of hint strings with services and managed controls
    """
    hints = []
    
    for control in aws_controls:
        hint_parts = []
        
        # Add services
        if control.services:
            services = ", ".join(control.services[:2])  # Limit to 2 services
            hint_parts.append(f"Services: {services}")
        
        # Add managed controls
        managed_parts = []
        if control.managed_controls.config_rules:
            rules = ", ".join(control.managed_controls.config_rules[:2])
            managed_parts.append(f"Config: {rules}")
        
        if control.managed_controls.security_hub_controls:
            hub_controls = ", ".join(control.managed_controls.security_hub_controls[:2])
            managed_parts.append(f"Security Hub: {hub_controls}")
        
        if control.managed_controls.control_tower_ids:
            ct_ids = ", ".join(control.managed_controls.control_tower_ids[:2])
            managed_parts.append(f"Control Tower: {ct_ids}")
        
        if managed_parts:
            hint_parts.append(" | ".join(managed_parts))
        
        # Build final hint
        if hint_parts:
            hint = f"• {control.title}\n  {' | '.join(hint_parts)}"
            hints.append(hint)
    
    return hints
