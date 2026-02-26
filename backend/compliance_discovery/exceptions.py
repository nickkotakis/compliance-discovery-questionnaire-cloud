"""Exception classes for the Compliance Discovery Questionnaire Tool."""


class ComplianceToolError(Exception):
    """Base exception for all compliance tool errors."""
    pass


# Parser Errors
class ProfileRetrievalError(ComplianceToolError):
    """Error retrieving OSCAL profile from NIST repository."""
    pass


class CatalogRetrievalError(ComplianceToolError):
    """Error retrieving OSCAL catalog from NIST repository."""
    pass


class InvalidFormatError(ComplianceToolError):
    """Error when OSCAL format is invalid or unexpected."""
    pass


class ParseError(ComplianceToolError):
    """Error parsing OSCAL data structures."""
    pass


class ControlNotFoundError(ComplianceToolError):
    """Error when a control specified in baseline is not found in catalog."""
    pass


# Framework Mapper Errors
class MappingDataError(ComplianceToolError):
    """Error loading or parsing framework mapping data."""
    pass


class FrameworkNotSupportedError(ComplianceToolError):
    """Error when an unsupported framework is requested."""
    pass


class MCPConnectionError(ComplianceToolError):
    """Error connecting to the compass-control-guides MCP server."""
    pass


class MCPQueryError(ComplianceToolError):
    """Error executing a query against the MCP server."""
    pass


class MCPResponseError(ComplianceToolError):
    """Error parsing or validating MCP server response."""
    pass


class AWSControlNotFoundError(ComplianceToolError):
    """Error when an AWS control is not found in MCP database."""
    pass


# Session Manager Errors
class SessionNotFoundError(ComplianceToolError):
    """Error when a session cannot be found."""
    pass


class InvalidStateError(ComplianceToolError):
    """Error when an operation is attempted in an invalid session state."""
    pass


class SessionPersistenceError(ComplianceToolError):
    """Error persisting or loading session data."""
    pass


class EvidenceNotFoundError(ComplianceToolError):
    """Error when evidence entry is not found."""
    pass


# Template Export Errors
class TemplateNotReadyError(ComplianceToolError):
    """Error when template export is attempted before all data is loaded.
    
    This error indicates that required data (controls, questions, or mappings)
    is not yet available for template generation.
    """
    pass


class TemplateGenerationError(ComplianceToolError):
    """Base error for template generation failures."""
    pass


class ExcelGenerationError(TemplateGenerationError):
    """Error generating Excel template."""
    pass


class PDFGenerationError(TemplateGenerationError):
    """Error generating PDF template."""
    pass
