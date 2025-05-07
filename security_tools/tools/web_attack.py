"""
Web Attack Tools
"""

from security_tools.core import HackingTool, HackingToolsCollection


class SqlmapTool(HackingTool):
    TITLE = "Sqlmap tool"
    DESCRIPTION = "Automatic SQL injection and database takeover tool"
    CATEGORY = "Web Attack"
    INSTALL_COMMANDS = ["sudo apt-get install sqlmap"]
    RUN_COMMANDS = ["sqlmap -h"]
    PROJECT_URL = "https://github.com/sqlmapproject/sqlmap"


class WebSploitTool(HackingTool):
    TITLE = "WebSploit"
    DESCRIPTION = "Advanced Web exploitation framework"
    CATEGORY = "Web Attack"
    INSTALL_COMMANDS = [
        "git clone https://github.com/The404Hacking/websploit.git",
        "cd websploit && pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd websploit && python websploit.py"]
    PROJECT_URL = "https://github.com/The404Hacking/websploit"


class SubDomainFinderTool(HackingTool):
    TITLE = "SubDomain Finder"
    DESCRIPTION = "Subdomain discovery tool to find subdomains of websites"
    CATEGORY = "Web Attack"
    INSTALL_COMMANDS = [
        "git clone https://github.com/aboul3la/Sublist3r.git",
        "cd Sublist3r && pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd Sublist3r && python sublist3r.py -h"]
    PROJECT_URL = "https://github.com/aboul3la/Sublist3r"


class CheckURLTool(HackingTool):
    TITLE = "CheckURL"
    DESCRIPTION = "Tool to check if a website is up or down"
    CATEGORY = "Web Attack"
    INSTALL_COMMANDS = ["git clone https://github.com/UndeadSec/checkURL.git"]
    RUN_COMMANDS = ["cd checkURL && python checkURL.py"]
    PROJECT_URL = "https://github.com/UndeadSec/checkURL"


class BlazyTool(HackingTool):
    TITLE = "Blazy"
    DESCRIPTION = "Modern login bruteforcer which also tests for CSRF, Clickjacking, etc."
    CATEGORY = "Web Attack"
    INSTALL_COMMANDS = [
        "git clone https://github.com/UltimateHackers/Blazy.git",
        "cd Blazy && pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd Blazy && python blazy.py"]
    PROJECT_URL = "https://github.com/UltimateHackers/Blazy"


class DSSSTool(HackingTool):
    TITLE = "Damn Small SQLi Scanner"
    DESCRIPTION = "A fully functional SQL injection vulnerability scanner"
    CATEGORY = "Web Attack"
    INSTALL_COMMANDS = ["git clone https://github.com/stamparm/DSSS.git"]
    RUN_COMMANDS = ["cd DSSS && python dsss.py"]
    PROJECT_URL = "https://github.com/stamparm/DSSS"


class XSSStrikeTool(HackingTool):
    TITLE = "XSStrike"
    DESCRIPTION = "Advanced XSS detection and exploitation suite"
    CATEGORY = "Web Attack"
    INSTALL_COMMANDS = [
        "git clone https://github.com/s0md3v/XSStrike.git",
        "cd XSStrike && pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd XSStrike && python xsstrike.py"]
    PROJECT_URL = "https://github.com/s0md3v/XSStrike"


class WebAttackTools(HackingToolsCollection):
    TITLE = "Web Attack Tools"
    DESCRIPTION = "Tools for web application security testing and exploitation"
    
    TOOLS = [
        SqlmapTool(),
        WebSploitTool(),
        SubDomainFinderTool(),
        CheckURLTool(),
        BlazyTool(),
        DSSSTool(),
        XSSStrikeTool()
    ]