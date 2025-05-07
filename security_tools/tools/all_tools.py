"""
Combined tools collection for the security tools dashboard
"""

from security_tools.core import HackingToolsCollection
from security_tools.tools.info_gathering import InformationGatheringTools
from security_tools.tools.web_attack import WebAttackTools
from security_tools.tools.anonymity import AnonymityTools
from security_tools.tools.forensic import ForensicTools
from security_tools.tools.password_tools import PasswordToolsCollection
from security_tools.tools.hardware_tools import HardwareToolsCollection
from security_tools.tools.custom_generator import CustomToolsCollection

class AllTools(HackingToolsCollection):
    TITLE = "All Security Tools"
    DESCRIPTION = "Complete collection of security tools integrated with the Dark Web Crawler"
    
    TOOLS = [
        InformationGatheringTools(),
        WebAttackTools(),
        AnonymityTools(),
        ForensicTools(),
        PasswordToolsCollection(),
        HardwareToolsCollection(),
        CustomToolsCollection()
    ]