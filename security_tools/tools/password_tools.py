"""
Password Cracking and Authentication Tools
"""

from security_tools.core import HackingTool, HackingToolsCollection


class HashcatTool(HackingTool):
    TITLE = "Hashcat"
    DESCRIPTION = "Advanced password recovery utility supporting hundreds of hash types"
    CATEGORY = "Password Tools"
    INSTALL_COMMANDS = ["sudo apt-get install hashcat"]
    RUN_COMMANDS = ["hashcat --help"]
    PROJECT_URL = "https://hashcat.net/hashcat/"


class JohnTheRipperTool(HackingTool):
    TITLE = "John the Ripper"
    DESCRIPTION = "Password security auditing and password recovery tool supporting various password hash types"
    CATEGORY = "Password Tools"
    INSTALL_COMMANDS = ["sudo apt-get install john"]
    RUN_COMMANDS = ["john --help"]
    PROJECT_URL = "https://www.openwall.com/john/"


class HydraFtpTool(HackingTool):
    TITLE = "Hydra FTP Cracker"
    DESCRIPTION = "Fast and flexible online password cracking tool for FTP servers"
    CATEGORY = "Password Tools"
    INSTALL_COMMANDS = ["sudo apt-get install hydra"]
    RUN_COMMANDS = ["hydra -h"]
    PROJECT_URL = "https://github.com/vanhauser-thc/thc-hydra"


class HydraSshTool(HackingTool):
    TITLE = "Hydra SSH Cracker"
    DESCRIPTION = "Fast and flexible online password cracking tool for SSH servers"
    CATEGORY = "Password Tools"
    INSTALL_COMMANDS = ["sudo apt-get install hydra"]
    RUN_COMMANDS = ["hydra -h"]
    PROJECT_URL = "https://github.com/vanhauser-thc/thc-hydra"


class XHydraGUITool(HackingTool):
    TITLE = "XHydra"
    DESCRIPTION = "Graphical user interface for the Hydra password cracking tool"
    CATEGORY = "Password Tools"
    INSTALL_COMMANDS = ["sudo apt-get install hydra-gtk"]
    RUN_COMMANDS = ["xhydra"]
    PROJECT_URL = "https://github.com/vanhauser-thc/thc-hydra"


class CredentialHarvesterTool(HackingTool):
    TITLE = "Credential Harvester"
    DESCRIPTION = "Tool for harvesting credentials from various sources"
    CATEGORY = "Password Tools"
    INSTALL_COMMANDS = [
        "git clone https://github.com/trustedsec/social-engineer-toolkit.git",
        "cd social-engineer-toolkit && sudo pip install -r requirements.txt",
        "cd social-engineer-toolkit && sudo python setup.py install"
    ]
    RUN_COMMANDS = ["sudo setoolkit"]
    PROJECT_URL = "https://github.com/trustedsec/social-engineer-toolkit"


class CudaHashcatTool(HackingTool):
    TITLE = "CUDA Hashcat"
    DESCRIPTION = "GPU-based password cracking tool with CUDA support for faster cracking"
    CATEGORY = "Password Tools"
    INSTALL_COMMANDS = ["sudo apt-get install hashcat"]
    RUN_COMMANDS = ["hashcat -h"]
    PROJECT_URL = "https://hashcat.net/hashcat/"


class OphcrackTool(HackingTool):
    TITLE = "Ophcrack"
    DESCRIPTION = "Windows password cracker using rainbow tables"
    CATEGORY = "Password Tools"
    INSTALL_COMMANDS = ["sudo apt-get install ophcrack"]
    RUN_COMMANDS = ["ophcrack"]
    PROJECT_URL = "https://ophcrack.sourceforge.io/"


class SqlmapAdvancedTool(HackingTool):
    TITLE = "SQLmap Advanced"
    DESCRIPTION = "Automated SQL injection tool for detecting and exploiting SQL vulnerabilities in databases and web applications"
    CATEGORY = "Password Tools"
    INSTALL_COMMANDS = [
        "git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev",
        "cd sqlmap-dev && sudo pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd sqlmap-dev && python sqlmap.py --help"]
    PROJECT_URL = "https://sqlmap.org/"
    
    def __init__(self):
        super().__init__(options=[
            ("Basic Scan", self.basic_scan),
            ("Database Fingerprint", self.db_fingerprint),
            ("Tables Enumeration", self.tables_enum),
            ("Data Extraction", self.data_extraction),
            ("Shell Access", self.shell_access),
            ("Database Dump", self.db_dump)
        ])
    
    def basic_scan(self):
        """Run a basic SQLmap scan"""
        url = input("\nEnter the target URL: ")
        command = f"cd sqlmap-dev && python sqlmap.py -u \"{url}\" --batch"
        print(f"\nRunning command: {command}")
        import os
        os.system(command)
        
    def db_fingerprint(self):
        """Perform database fingerprinting"""
        url = input("\nEnter the target URL: ")
        command = f"cd sqlmap-dev && python sqlmap.py -u \"{url}\" --fingerprint --batch"
        print(f"\nRunning command: {command}")
        import os
        os.system(command)
        
    def tables_enum(self):
        """Enumerate database tables"""
        url = input("\nEnter the target URL: ")
        command = f"cd sqlmap-dev && python sqlmap.py -u \"{url}\" --tables --batch"
        print(f"\nRunning command: {command}")
        import os
        os.system(command)
        
    def data_extraction(self):
        """Extract data from database"""
        url = input("\nEnter the target URL: ")
        table = input("Enter table name to extract: ")
        command = f"cd sqlmap-dev && python sqlmap.py -u \"{url}\" -T \"{table}\" --dump --batch"
        print(f"\nRunning command: {command}")
        import os
        os.system(command)
        
    def shell_access(self):
        """Get a shell on the database server"""
        url = input("\nEnter the target URL: ")
        command = f"cd sqlmap-dev && python sqlmap.py -u \"{url}\" --os-shell --batch"
        print(f"\nRunning command: {command}")
        import os
        os.system(command)
        
    def db_dump(self):
        """Dump the entire database"""
        url = input("\nEnter the target URL: ")
        command = f"cd sqlmap-dev && python sqlmap.py -u \"{url}\" --dump-all --batch"
        print(f"\nRunning command: {command}")
        import os
        os.system(command)


class PasswordToolsCollection(HackingToolsCollection):
    TITLE = "Password & Authentication Tools"
    DESCRIPTION = "Tools for password cracking, auditing and SQL injection"
    
    TOOLS = [
        HashcatTool(),
        JohnTheRipperTool(),
        HydraFtpTool(),
        HydraSshTool(),
        XHydraGUITool(),
        CredentialHarvesterTool(),
        CudaHashcatTool(),
        OphcrackTool(),
        SqlmapAdvancedTool()
    ]