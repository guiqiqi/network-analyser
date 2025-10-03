from ..plugin import Plugin

from .traceroute import TraceRoute
from .dns import DNS
from .ifconfig import IFConfig
from .external import ExternalIP

try:
    from .wifi import WiFi
except NotImplementedError:
    WiFi = None

__all__ = ['Plugin', 'IFConfig', 'TraceRoute', 'DNS', 'WiFi', 'ExternalIP']
