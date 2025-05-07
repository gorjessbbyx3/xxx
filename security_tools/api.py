"""
API for integrating security tools with the web interface
"""

from typing import List, Dict, Any, Optional
import logging
import json

from security_tools.manager import SecurityToolsManager
from security_tools.tools.all_tools import AllTools

# Set up logging
logger = logging.getLogger('security_tools.api')

class SecurityToolsAPI:
    """
    API for accessing security tools functionality from the web interface
    """
    
    def __init__(self):
        """Initialize the security tools API"""
        self.all_tools = AllTools()
        self.manager = SecurityToolsManager(self.all_tools)
        
    def get_categories(self) -> List[str]:
        """
        Get list of all tool categories
        
        Returns:
            List of category names
        """
        categories = {}
        tools_by_category = self.manager.get_tools_by_category()
        return list(tools_by_category.keys())
        
    def get_tools_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get tools organized by category
        
        Returns:
            Dictionary with categories as keys and lists of tools as values
        """
        return self.manager.get_tools_by_category()
        
    def get_all_tools(self) -> List[Dict[str, Any]]:
        """
        Get information about all available tools
        
        Returns:
            List of dictionaries with tool information
        """
        return self.manager.get_all_tools()
        
    def search_tools(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for tools matching the query
        
        Args:
            query: Search query string
            
        Returns:
            List of matching tools
        """
        return self.manager.search_tools(query)
        
    def execute_tool(self, tool_name: str, action: str) -> Dict[str, Any]:
        """
        Execute a specific action on a tool
        
        Args:
            tool_name: Name of the tool to execute
            action: Action to perform (install, run, etc.)
            
        Returns:
            Dictionary with execution result
        """
        return self.manager.execute_tool(tool_name, action)
        
    def get_tool_details(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific tool
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dictionary with tool details or None if not found
        """
        return self.manager.get_tool_by_name(tool_name)
        
    def export_tools_json(self) -> str:
        """
        Export all tools to JSON string
        
        Returns:
            JSON string with tools data
        """
        tools = self.manager.get_all_tools()
        return json.dumps(tools, indent=2)
        
    def get_total_tools_count(self) -> int:
        """
        Get total number of available tools
        
        Returns:
            Total count of tools
        """
        return len(self.manager.get_all_tools())