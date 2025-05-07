"""
Digital Forensics Tools
"""

from security_tools.core import HackingTool, HackingToolsCollection


class AutopsyTool(HackingTool):
    TITLE = "Autopsy"
    DESCRIPTION = "Digital forensics platform for analyzing disk images and recovering files"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install autopsy"]
    RUN_COMMANDS = ["autopsy"]
    PROJECT_URL = "https://www.autopsy.com/"


class WiresharkTool(HackingTool):
    TITLE = "Wireshark"
    DESCRIPTION = "Network protocol analyzer for examining network traffic"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install wireshark"]
    RUN_COMMANDS = ["wireshark"]
    PROJECT_URL = "https://www.wireshark.org/"


class BulkExtractorTool(HackingTool):
    TITLE = "Bulk Extractor"
    DESCRIPTION = "Extracts useful information without parsing filesystem structure"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install bulk-extractor"]
    RUN_COMMANDS = ["bulk_extractor -h"]
    PROJECT_URL = "https://github.com/simsong/bulk_extractor"


class DiskImageAcquireTool(HackingTool):
    TITLE = "Disk Clone and ISO Image Acquire"
    DESCRIPTION = "Create forensically sound disk images for analysis"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install guymager"]
    RUN_COMMANDS = ["guymager"]
    PROJECT_URL = "https://guymager.sourceforge.io/"


class VolatilityTool(HackingTool):
    TITLE = "Volatility3"
    DESCRIPTION = "Advanced memory forensics framework for analyzing RAM dumps"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = [
        "git clone https://github.com/volatilityfoundation/volatility3.git",
        "cd volatility3 && pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd volatility3 && python vol.py -h"]
    PROJECT_URL = "https://github.com/volatilityfoundation/volatility3/"


class ForemanTool(HackingTool):
    TITLE = "Foremost"
    DESCRIPTION = "File recovery tool based on file headers and footers"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install foremost"]
    RUN_COMMANDS = ["foremost -h"]
    PROJECT_URL = "http://foremost.sourceforge.net/"


class BinwalkTool(HackingTool):
    TITLE = "Binwalk"
    DESCRIPTION = "Firmware analysis tool for searching embedded files and executable code"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install binwalk"]
    RUN_COMMANDS = ["binwalk -h"]
    PROJECT_URL = "https://github.com/ReFirmLabs/binwalk"


class ForensicTools(HackingToolsCollection):
    TITLE = "Forensic Tools"
    DESCRIPTION = "Tools for digital forensics and incident response"
    
    TOOLS = [
        AutopsyTool(),
        WiresharkTool(),
        BulkExtractorTool(),
        DiskImageAcquireTool(),
        VolatilityTool(),
        ForemanTool(),
        BinwalkTool()
    ]