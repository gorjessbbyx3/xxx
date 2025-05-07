"""
Core security tools adapter for the Dark Web Crawler
Based on core.py from the HackingTool project
"""

import os
import sys
import webbrowser
from platform import system
from traceback import print_exc
from typing import Callable, List, Tuple, Any, Dict, Optional

def clear_screen():
    """Clear the terminal screen"""
    os.system("cls" if system() == "Windows" else "clear")

def validate_input(ip, val_range):
    """Validate user input against a range of valid values"""
    val_range = val_range or []
    try:
        ip = int(ip)
        if ip in val_range:
            return ip
    except Exception:
        return None
    return None

class HackingTool:
    """
    Base class for all hacking tools
    """
    # About the HackingTool
    TITLE: str = ""  # used to show info in the menu
    DESCRIPTION: str = ""
    CATEGORY: str = ""  # category for organization and filtering
    
    # Installation and execution commands
    INSTALL_COMMANDS: List[str] = []
    INSTALLATION_DIR: str = ""
    UNINSTALL_COMMANDS: List[str] = []
    RUN_COMMANDS: List[str] = []
    
    # Additional options
    OPTIONS: List[Tuple[str, Callable]] = []
    PROJECT_URL: str = ""

    def __init__(self, options=None, installable: bool = True, runnable: bool = True):
        """
        Initialize the hacking tool with options
        
        Args:
            options: List of option tuples (name, function)
            installable: Whether this tool can be installed
            runnable: Whether this tool can be run
        """
        options = options or []
        if isinstance(options, list):
            self.OPTIONS = []
            if installable:
                self.OPTIONS.append(('Install', self.install))
            if runnable:
                self.OPTIONS.append(('Run', self.run))
            self.OPTIONS.extend(options)
        else:
            raise Exception(
                "options must be a list of (option_name, option_fn) tuples")

    def show_info(self):
        """Display information about the tool"""
        desc = self.DESCRIPTION
        if self.PROJECT_URL:
            desc += '\n\t[*] '
            desc += self.PROJECT_URL
        print(f"\n[*] {self.TITLE}")
        print(f"[-] {desc}")

    def show_options(self, parent=None):
        """
        Show available options for this tool
        
        Args:
            parent: Parent menu if applicable
            
        Returns:
            Return code for menu navigation
        """
        clear_screen()
        self.show_info()
        for index, option in enumerate(self.OPTIONS):
            print(f"[{index + 1}] {option[0]}")
        if self.PROJECT_URL:
            print(f"[{98}] Open project page")
        print(f"[{99}] Back to {parent.TITLE if parent is not None else 'Exit'}")
        
        option_index = input("Select an option : ").strip()
        try:
            option_index = int(option_index)
            if option_index - 1 in range(len(self.OPTIONS)):
                ret_code = self.OPTIONS[option_index - 1][1]()
                if ret_code != 99:
                    input("\n\nPress ENTER to continue:").strip()
            elif option_index == 98:
                self.show_project_page()
            elif option_index == 99:
                if parent is None:
                    sys.exit()
                return 99
        except (TypeError, ValueError):
            print("Please enter a valid option")
            input("\n\nPress ENTER to continue:").strip()
        except Exception:
            print_exc()
            input("\n\nPress ENTER to continue:").strip()
        return self.show_options(parent=parent)

    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the tool as a dictionary
        
        Returns:
            Dictionary with tool info
        """
        return {
            "title": self.TITLE,
            "description": self.DESCRIPTION,
            "category": self.CATEGORY,
            "project_url": self.PROJECT_URL,
            "installable": len(self.INSTALL_COMMANDS) > 0,
            "runnable": len(self.RUN_COMMANDS) > 0
        }

    def before_install(self):
        """Hook called before installation"""
        pass

    def install(self):
        """Install the tool"""
        self.before_install()
        if isinstance(self.INSTALL_COMMANDS, (list, tuple)):
            for INSTALL_COMMAND in self.INSTALL_COMMANDS:
                os.system(INSTALL_COMMAND)
            self.after_install()

    def after_install(self):
        """Hook called after installation"""
        print("Successfully installed!")

    def before_uninstall(self) -> bool:
        """
        Ask for confirmation from the user and return
        
        Returns:
            Boolean indicating whether to proceed with uninstallation
        """
        return True

    def uninstall(self):
        """Uninstall the tool"""
        if self.before_uninstall():
            if isinstance(self.UNINSTALL_COMMANDS, (list, tuple)):
                for UNINSTALL_COMMAND in self.UNINSTALL_COMMANDS:
                    os.system(UNINSTALL_COMMAND)
            self.after_uninstall()

    def after_uninstall(self):
        """Hook called after uninstallation"""
        pass

    def before_run(self):
        """Hook called before running the tool"""
        pass

    def run(self):
        """Run the tool"""
        self.before_run()
        if isinstance(self.RUN_COMMANDS, (list, tuple)):
            for RUN_COMMAND in self.RUN_COMMANDS:
                os.system(RUN_COMMAND)
            self.after_run()

    def after_run(self):
        """Hook called after running the tool"""
        pass

    def is_installed(self, dir_to_check=None) -> bool:
        """
        Check if the tool is installed
        
        Args:
            dir_to_check: Optional directory to check
            
        Returns:
            Boolean indicating if the tool is installed
        """
        if dir_to_check:
            return os.path.isdir(dir_to_check)
        elif self.INSTALLATION_DIR:
            return os.path.isdir(self.INSTALLATION_DIR)
        return False

    def show_project_page(self):
        """Open the project page in a web browser"""
        if self.PROJECT_URL:
            webbrowser.open_new_tab(self.PROJECT_URL)


class HackingToolsCollection:
    """
    Collection of multiple hacking tools
    """
    TITLE: str = ""  # used to show info in the menu
    DESCRIPTION: str = ""
    TOOLS = []  # type: List[Any[HackingTool, HackingToolsCollection]]

    def __init__(self):
        """Initialize the tools collection"""
        pass

    def show_info(self):
        """Display information about the collection"""
        print(f"\n[*] {self.TITLE}")
        print(f"[-] {self.DESCRIPTION}")

    def show_options(self, parent=None):
        """
        Show available tools in this collection
        
        Args:
            parent: Parent menu if applicable
            
        Returns:
            Return code for menu navigation
        """
        clear_screen()
        self.show_info()
        for index, tool in enumerate(self.TOOLS):
            print(f"[{index}] {tool.TITLE}")
        print(f"[{99}] Back to {parent.TITLE if parent is not None else 'Exit'}")
        
        tool_index = input("Choose a tool to proceed: ").strip()
        try:
            tool_index = int(tool_index)
            if tool_index in range(len(self.TOOLS)):
                ret_code = self.TOOLS[tool_index].show_options(parent=self)
                if ret_code != 99:
                    input("\n\nPress ENTER to continue:").strip()
            elif tool_index == 99:
                if parent is None:
                    sys.exit()
                return 99
        except (TypeError, ValueError):
            print("Please enter a valid option")
            input("\n\nPress ENTER to continue:").strip()
        except Exception:
            print_exc()
            input("\n\nPress ENTER to continue:").strip()
        return self.show_options(parent=parent)
        
    def get_all_tools(self) -> List[Dict[str, Any]]:
        """
        Get information about all tools in this collection
        
        Returns:
            List of dictionaries with tool information
        """
        result = []
        
        for tool in self.TOOLS:
            if isinstance(tool, HackingTool):
                result.append(tool.get_info())
            elif isinstance(tool, HackingToolsCollection):
                # Add the category information
                category_tools = tool.get_all_tools()
                for t in category_tools:
                    if not t.get("category"):
                        t["category"] = tool.TITLE
                result.extend(category_tools)
                
        return result
        
    def get_tool_by_name(self, name: str) -> Optional[HackingTool]:
        """
        Find a tool by its name
        
        Args:
            name: Name of the tool to find
            
        Returns:
            HackingTool instance or None if not found
        """
        for tool in self.TOOLS:
            if isinstance(tool, HackingTool) and tool.TITLE == name:
                return tool
            elif isinstance(tool, HackingToolsCollection):
                found_tool = tool.get_tool_by_name(name)
                if found_tool:
                    return found_tool
        
        return None