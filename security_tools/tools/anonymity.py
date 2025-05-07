"""
Anonymity and Privacy Tools
"""

from security_tools.core import HackingTool, HackingToolsCollection


class AnonsurfTool(HackingTool):
    TITLE = "Anonsurf"
    DESCRIPTION = "A tool designed to make system-wide modifications for anonymizing all internet traffic"
    CATEGORY = "Anonymity Tools"
    INSTALL_COMMANDS = [
        "git clone https://github.com/Und3rf10w/kali-anonsurf.git",
        "cd kali-anonsurf && sudo ./installer.sh"
    ]
    RUN_COMMANDS = ["sudo anonsurf start"]
    PROJECT_URL = "https://github.com/Und3rf10w/kali-anonsurf"


class MultitorTool(HackingTool):
    TITLE = "Multitor"
    DESCRIPTION = "Create multiple TOR instances with a load-balancing feature"
    CATEGORY = "Anonymity Tools"
    INSTALL_COMMANDS = ["git clone https://github.com/trimstray/multitor.git"]
    RUN_COMMANDS = ["cd multitor && bash multitor.sh --help"]
    PROJECT_URL = "https://github.com/trimstray/multitor"


class TorIpChangerTool(HackingTool):
    TITLE = "Tor IP Changer"
    DESCRIPTION = "Automatically changes your IP address at regular intervals through TOR"
    CATEGORY = "Anonymity Tools"
    INSTALL_COMMANDS = [
        "git clone https://github.com/ruped24/toriptables2.git",
        "cd toriptables2 && sudo pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd toriptables2 && sudo python toriptables2.py -h"]
    PROJECT_URL = "https://github.com/ruped24/toriptables2"


class ProxyChainsTool(HackingTool):
    TITLE = "ProxyChains"
    DESCRIPTION = "Force any TCP connection through proxy like TOR or any other proxy"
    CATEGORY = "Anonymity Tools"
    INSTALL_COMMANDS = ["sudo apt-get install proxychains"]
    RUN_COMMANDS = ["proxychains"]
    PROJECT_URL = "https://github.com/haad/proxychains"


class MacChangerTool(HackingTool):
    TITLE = "MAC Changer"
    DESCRIPTION = "Change your MAC address to remain anonymous on networks"
    CATEGORY = "Anonymity Tools"
    INSTALL_COMMANDS = ["sudo apt-get install macchanger"]
    RUN_COMMANDS = ["sudo macchanger --help"]
    PROJECT_URL = "https://github.com/alobbs/macchanger"


class AnonymityTools(HackingToolsCollection):
    TITLE = "Anonymity Tools"
    DESCRIPTION = "Tools for maintaining privacy and anonymity online"
    
    TOOLS = [
        AnonsurfTool(),
        MultitorTool(),
        TorIpChangerTool(),
        ProxyChainsTool(),
        MacChangerTool()
    ]