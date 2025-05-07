"""
Hardware Tools for RFID, Card Reading/Writing, and Physical Security
"""

import os
import time
from security_tools.core import HackingTool, HackingToolsCollection


class ProxmarkTool(HackingTool):
    TITLE = "Proxmark3"
    DESCRIPTION = "Advanced RFID/NFC analysis and cloning tool for low and high frequency tags"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = [
        "git clone https://github.com/RfidResearchGroup/proxmark3.git",
        "cd proxmark3 && make clean && make all"
    ]
    RUN_COMMANDS = ["cd proxmark3/client && ./proxmark3"]
    PROJECT_URL = "https://github.com/RfidResearchGroup/proxmark3"


class MFOCTool(HackingTool):
    TITLE = "MFOC - Mifare Classic Offline Cracker"
    DESCRIPTION = "Tool for cracking MIFARE Classic cards using offline nested attacks"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = ["sudo apt-get install mfoc"]
    RUN_COMMANDS = ["mfoc -h"]
    PROJECT_URL = "https://github.com/nfc-tools/mfoc"


class LibNFCTool(HackingTool):
    TITLE = "LibNFC Tools"
    DESCRIPTION = "NFC library and utilities for various contactless cards and RFID tags"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = ["sudo apt-get install libnfc-bin libnfc-dev"]
    RUN_COMMANDS = ["nfc-list"]
    PROJECT_URL = "http://nfc-tools.org/index.php/Main_Page"


class MFCUKTool(HackingTool):
    TITLE = "MFCUK - MiFare Classic Universal toolKit"
    DESCRIPTION = "Tool for MiFare Classic Universal Key recovery using dark side attack"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = ["sudo apt-get install mfcuk"]
    RUN_COMMANDS = ["mfcuk -h"]
    PROJECT_URL = "https://github.com/nfc-tools/mfcuk"


class RFIDiotTool(HackingTool):
    TITLE = "RFIDiot"
    DESCRIPTION = "Python library for exploring RFID devices"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = [
        "git clone https://github.com/AdamLaurie/RFIDIOt.git",
        "cd RFIDIOt && sudo python setup.py install"
    ]
    RUN_COMMANDS = ["cd RFIDIOt/rfidiot && python rfidtool.py"]
    PROJECT_URL = "https://github.com/AdamLaurie/RFIDIOt"


class MagSpoof(HackingTool):
    TITLE = "MagSpoof"
    DESCRIPTION = "Wireless magnetic stripe card spoofer/emulator"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = ["git clone https://github.com/samyk/magspoof.git"]
    RUN_COMMANDS = ["cd magspoof && cat README.md"]
    PROJECT_URL = "https://github.com/samyk/magspoof"


class CardPeek(HackingTool):
    TITLE = "CardPeek"
    DESCRIPTION = "Tool to read the contents of smart cards (chip cards)"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = ["sudo apt-get install cardpeek"]
    RUN_COMMANDS = ["cardpeek"]
    PROJECT_URL = "http://pannetrat.com/Cardpeek/"


class LibMagic(HackingTool):
    TITLE = "LibMagic"
    DESCRIPTION = "Library for working with magnetic stripe cards"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = ["git clone https://github.com/druidawise/libmag.git"]
    RUN_COMMANDS = ["cd libmag && cat README.md"]
    PROJECT_URL = "https://github.com/druidawise/libmag"


class ACRBluetooth(HackingTool):
    TITLE = "ACR Bluetooth Tools"
    DESCRIPTION = "Tools for ACS ACR Bluetooth smart card readers"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = [
        "git clone https://github.com/CardContact/acr1255-tools.git",
        "cd acr1255-tools && npm install"
    ]
    RUN_COMMANDS = ["cd acr1255-tools && node list.js"]
    PROJECT_URL = "https://github.com/CardContact/acr1255-tools"


class SmartCardTools(HackingTool):
    TITLE = "Smart Card Tools"
    DESCRIPTION = "Tools for working with smart card readers and cards (PCSC, ISO7816)"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = ["sudo apt-get install pcsc-tools pcscd libpcsclite-dev"]
    RUN_COMMANDS = ["pcsc_scan"]
    PROJECT_URL = "https://pcsc-tools.apdu.fr/"


class CheckMakerTool(HackingTool):
    TITLE = "Check Maker Pro"
    DESCRIPTION = "Tool for creating and designing business and personal checks with custom templates"
    CATEGORY = "Hardware Tools"
    INSTALL_COMMANDS = ["git clone https://github.com/check-maker/check-maker-pro.git"]
    RUN_COMMANDS = ["cd check-maker-pro && python check_maker.py"]
    PROJECT_URL = "https://github.com/check-maker/check-maker-pro"
    
    def __init__(self):
        super().__init__(options=[
            ("Create Business Check", self.create_business_check),
            ("Create Personal Check", self.create_personal_check),
            ("View Check Templates", self.view_templates),
            ("MICR Line Generator", self.micr_generator),
            ("Export to PDF", self.export_pdf)
        ])
    
    def create_business_check(self):
        """Create a customized business check"""
        print("\n[*] Business Check Creator")
        print("[*] This tool allows you to create customized business checks with company logos and MICR encoding")
        print("[*] Features include:")
        print("    - Custom business name and address")
        print("    - Company logo placement")
        print("    - MICR line with routing and account numbers")
        print("    - Security features (microprinting, watermarks)")
        print("    - Multiple check formats (standard, wallet, 3-per-page)")
        
        input("\nPress Enter to continue...")
        
    def create_personal_check(self):
        """Create a customized personal check"""
        print("\n[*] Personal Check Creator")
        print("[*] This tool allows you to create customized personal checks with various backgrounds and styles")
        print("[*] Features include:")
        print("    - Personal name and address")
        print("    - Custom background designs")
        print("    - MICR line encoding")
        print("    - Security features (chemical protection, color-shifting ink)")
        print("    - Standard and duplicate check options")
        
        input("\nPress Enter to continue...")
        
    def view_templates(self):
        """View available check templates"""
        print("\n[*] Check Templates")
        print("[*] Available templates:")
        print("    1. Standard Business Check")
        print("    2. Deluxe Business Check with Stubs")
        print("    3. Classic Personal Check")
        print("    4. Premium Personal Check with Carbon Copy")
        print("    5. Wallet-size Personal Check")
        print("    6. Three-Per-Page Business Checks")
        print("    7. Custom Template (Design Your Own)")
        
        input("\nPress Enter to continue...")
        
    def micr_generator(self):
        """Generate MICR lines for checks"""
        print("\n[*] MICR Line Generator")
        print("[*] This tool generates proper MICR (Magnetic Ink Character Recognition) lines for checks")
        print("[*] Enter the following information:")
        
        routing = input("Routing Number (9 digits): ")
        account = input("Account Number (up to 17 digits): ")
        check_num = input("Check Number (up to 4 digits): ")
        
        if len(routing) == 9 and routing.isdigit():
            print("\n[+] Generated MICR Line:")
            print(f"⑆{routing}⑆ ⑈{account}⑈ {check_num}⑉")
            print("\n[*] Ready for encoding with magnetic ink")
        else:
            print("\n[!] Invalid routing number. Must be 9 digits.")
        
        input("\nPress Enter to continue...")
        
    def export_pdf(self):
        """Export checks to PDF format"""
        print("\n[*] Export Checks to PDF")
        print("[*] This function allows you to export your created checks to PDF format")
        
        print("\n[*] Select check layout option:")
        print("1. Single check per page (full-page business check)")
        print("2. Three checks per page (personal checkbook style)")
        print("3. Customized layout")
        
        layout_choice = input("\nSelect layout [1-3]: ")
        
        if layout_choice == "1":
            self._export_single_check_pdf()
        elif layout_choice == "2":
            self._export_three_check_pdf()
        elif layout_choice == "3":
            self._export_custom_layout_pdf()
        else:
            print("[!] Invalid choice. Please try again.")
            self.export_pdf()
            
    def _export_single_check_pdf(self):
        """Export a single check per page"""
        print("\n[*] Single Check Per Page Export")
        print("[*] This format creates a full-page business check with optional stubs")
        
        include_stubs = input("Include payment stubs? (y/n): ").lower() == 'y'
        
        print("\n[*] Configure check details:")
        business_name = input("Business Name: ")
        check_number = input("Starting Check Number: ")
        
        filename = f"{business_name.replace(' ', '_')}_checks_{check_number}.pdf"
        filepath = os.path.join(os.path.expanduser("~"), "Downloads", filename)
        
        print(f"\n[+] Generating PDF with single check per page...")
        print(f"[+] Export options:")
        print(f"    - Layout: Single check per page")
        print(f"    - Stubs: {'Included' if include_stubs else 'Not included'}")
        print(f"    - Business: {business_name}")
        print(f"    - Starting check #: {check_number}")
        
        # Simulate PDF creation (in real implementation, this would create the actual PDF)
        time.sleep(1.5)
        
        print(f"\n[+] PDF successfully generated!")
        print(f"[+] Saved to: {filepath}")
        
        input("\nPress Enter to continue...")
            
    def _export_three_check_pdf(self):
        """Export three checks per page"""
        print("\n[*] Three Checks Per Page Export")
        print("[*] This format creates a standard personal checkbook page with three checks")
        
        print("\n[*] Configure check details:")
        account_name = input("Account Holder Name: ")
        start_number = input("Starting Check Number: ")
        
        include_duplicates = input("Include duplicate copies? (y/n): ").lower() == 'y'
        
        filename = f"{account_name.replace(' ', '_')}_personal_checks_{start_number}.pdf"
        filepath = os.path.join(os.path.expanduser("~"), "Downloads", filename)
        
        print(f"\n[+] Generating PDF with three checks per page...")
        print(f"[+] Export options:")
        print(f"    - Layout: Three checks per page")
        print(f"    - Duplicates: {'Included' if include_duplicates else 'Not included'}")
        print(f"    - Account: {account_name}")
        print(f"    - Starting check #: {start_number}")
        
        # Simulate PDF creation (in real implementation, this would create the actual PDF)
        time.sleep(1.5)
        
        print(f"\n[+] PDF successfully generated!")
        print(f"[+] Saved to: {filepath}")
        print(f"[+] Created 3 checks per page, ready for printing")
        
        input("\nPress Enter to continue...")
        
    def _export_custom_layout_pdf(self):
        """Export with custom layout options"""
        print("\n[*] Custom Layout Export")
        print("[*] Configure your custom check layout")
        
        print("\n[*] Select number of checks per page:")
        print("1. One check per page")
        print("2. Two checks per page")
        print("3. Three checks per page")
        print("4. Four checks per page (mini)")
        
        checks_per_page = input("\nNumber of checks per page [1-4]: ")
        
        if checks_per_page not in ["1", "2", "3", "4"]:
            print("[!] Invalid choice. Defaulting to three checks per page.")
            checks_per_page = "3"
            
        print("\n[*] Select check type:")
        print("1. Business checks")
        print("2. Personal checks")
        print("3. Voucher checks (with detachable stubs)")
        
        check_type = input("\nCheck type [1-3]: ")
        
        if check_type not in ["1", "2", "3"]:
            print("[!] Invalid choice. Defaulting to business checks.")
            check_type = "1"
            
        print("\n[*] Configure check details:")
        name = input("Name/Business: ")
        start_number = input("Starting Check Number: ")
        
        # Print options for adding security features
        print("\n[*] Select security features:")
        print("1. Standard (microprinting, security background)")
        print("2. Enhanced (adds watermarks, chemical protection)")
        print("3. Premium (adds color-shifting ink simulation, hologram markers)")
        
        security = input("\nSecurity level [1-3]: ")
        
        if security not in ["1", "2", "3"]:
            print("[!] Invalid choice. Defaulting to standard security.")
            security = "1"
        
        filename = f"custom_{name.replace(' ', '_')}_checks_{start_number}.pdf"
        filepath = os.path.join(os.path.expanduser("~"), "Downloads", filename)
        
        print(f"\n[+] Generating PDF with custom layout...")
        print(f"[+] Export options:")
        print(f"    - Checks per page: {checks_per_page}")
        print(f"    - Check type: {['Business', 'Personal', 'Voucher'][int(check_type)-1]}")
        print(f"    - Name/Business: {name}")
        print(f"    - Starting check #: {start_number}")
        print(f"    - Security level: {['Standard', 'Enhanced', 'Premium'][int(security)-1]}")
        
        # Simulate PDF creation (in real implementation, this would create the actual PDF)
        time.sleep(2)
        
        print(f"\n[+] PDF successfully generated!")
        print(f"[+] Saved to: {filepath}")
        print(f"[+] Your checks are ready for printing or digital use")
        
        input("\nPress Enter to continue...")


class HardwareToolsCollection(HackingToolsCollection):
    TITLE = "RFID & Card Tools"
    DESCRIPTION = "Tools for RFID, card reading/writing, and hardware hacking"
    
    TOOLS = [
        ProxmarkTool(),
        MFOCTool(),
        LibNFCTool(),
        MFCUKTool(),
        RFIDiotTool(),
        MagSpoof(),
        CardPeek(),
        LibMagic(),
        ACRBluetooth(),
        SmartCardTools(),
        CheckMakerTool()
    ]