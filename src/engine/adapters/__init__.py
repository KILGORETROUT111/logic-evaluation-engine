from .base import AdapterProtocol, AdapterRegistry  # re-export
# Side-effect imports to ensure registration:
from .legal import LegalAdapter  # noqa: F401
from .medical import MedicalAdapter  # noqa: F401
