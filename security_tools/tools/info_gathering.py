"""
Information Gathering Tools
"""

from security_tools.core import HackingTool, HackingToolsCollection

class NmapTool(HackingTool):
    TITLE = "Network Map (nmap)"
    DESCRIPTION = "Network scanning tool to discover hosts and services on a computer network"
    CATEGORY = "Information Gathering"
    INSTALL_COMMANDS = ["sudo apt-get install nmap"]
    RUN_COMMANDS = ["nmap"]
    PROJECT_URL = "https://nmap.org/"


class ReconDogTool(HackingTool):
    TITLE = "ReconDog"
    DESCRIPTION = "All-in-one tool for all your reconnaissance needs"
    CATEGORY = "Information Gathering"
    INSTALL_COMMANDS = [
        "git clone https://github.com/s0md3v/ReconDog",
        "cd ReconDog && pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd ReconDog && python dog"]
    PROJECT_URL = "https://github.com/s0md3v/ReconDog"


class InfogaTool(HackingTool):
    TITLE = "Infoga - Email OSINT"
    DESCRIPTION = "Email OSINT tool for gathering information about email addresses"
    CATEGORY = "Information Gathering"
    INSTALL_COMMANDS = [
        "git clone https://github.com/m4ll0k/Infoga.git",
        "cd Infoga && pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd Infoga && python infoga.py"]
    PROJECT_URL = "https://github.com/m4ll0k/Infoga"


class ReconSpiderTool(HackingTool):
    TITLE = "ReconSpider"
    DESCRIPTION = "Advanced Open Source Intelligence (OSINT) Framework for scanning IP, Domains, and more"
    CATEGORY = "Information Gathering"
    INSTALL_COMMANDS = [
        "git clone https://github.com/bhavsec/reconspider.git",
        "cd reconspider && sudo python setup.py install"
    ]
    RUN_COMMANDS = ["cd reconspider && python reconspider.py"]
    PROJECT_URL = "https://github.com/bhavsec/reconspider"


class ShodanfyTool(HackingTool):
    TITLE = "Find Info Using Shodan"
    DESCRIPTION = "Shodan is a search engine for Internet-connected devices"
    CATEGORY = "Information Gathering"
    INSTALL_COMMANDS = [
        "git clone https://github.com/m4ll0k/Shodanfy.py.git",
        "cd Shodanfy.py && pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd Shodanfy.py && python shodanfy.py"]
    PROJECT_URL = "https://github.com/m4ll0k/Shodanfy.py"


class PortScannerRangerTool(HackingTool):
    TITLE = "Port Scanner - Ranger"
    DESCRIPTION = "Multi-threaded port scanner with customizable options"
    CATEGORY = "Information Gathering"
    INSTALL_COMMANDS = [
        "git clone https://github.com/joeyagreco/ranger-reloaded.git",
        "cd ranger-reloaded && pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd ranger-reloaded && python ranger_reloaded.py"]
    PROJECT_URL = "https://github.com/joeyagreco/ranger-reloaded"


class RedHawkTool(HackingTool):
    TITLE = "RED HAWK (All In One Scanning)"
    DESCRIPTION = "All in one tool for Information Gathering and Vulnerability Scanning"
    CATEGORY = "Information Gathering"
    INSTALL_COMMANDS = ["git clone https://github.com/Tuhinshubhra/RED_HAWK.git"]
    RUN_COMMANDS = ["cd RED_HAWK && php rhawk.php"]
    PROJECT_URL = "https://github.com/Tuhinshubhra/RED_HAWK"


class InformationGatheringTools(HackingToolsCollection):
    TITLE = "Information Gathering Tools"
    DESCRIPTION = "Tools for reconnaissance and information collection"
    
    TOOLS = [
        NmapTool(),
        ReconDogTool(),
        InfogaTool(),
        ReconSpiderTool(),
        ShodanfyTool(),
        PortScannerRangerTool(),
        RedHawkTool()
    ]