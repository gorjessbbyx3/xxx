"""
Security tools manager for the Dark Web Crawler
"""

from typing import List, Dict, Any, Optional
import os
import json
import logging

from security_tools.core import HackingTool, HackingToolsCollection

# Set up logging
logger = logging.getLogger('security_tools.manager')

class SecurityToolsManager:
    """
    Manager class for security tools integration
    """
    
    def __init__(self, tools_collection=None):
        """
        Initialize the security tools manager
        
        Args:
            tools_collection: HackingToolsCollection instance to manage
        """
        self.tools_collection = tools_collection
        self.tools_cache = None
        
    def get_all_tools(self) -> List[Dict[str, Any]]:
        """
        Get information about all available tools
        
        Returns:
            List of dictionaries with tool information
        """
        if self.tools_collection:
            if not self.tools_cache:
                self.tools_cache = self.tools_collection.get_all_tools()
            return self.tools_cache
        
        # Return empty list if no tools collection is set
        return []
    
    def get_tools_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get tools organized by category
        
        Returns:
            Dictionary with categories as keys and lists of tools as values
        """
        tools = self.get_all_tools()
        result = {}
        
        for tool in tools:
            category = tool.get("category", "Uncategorized")
            if category not in result:
                result[category] = []
            result[category].append(tool)
            
        return result
    
    def get_tool_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Find a tool by its name
        
        Args:
            name: Name of the tool to find
            
        Returns:
            Tool info dictionary or None if not found
        """
        tools = self.get_all_tools()
        for tool in tools:
            if tool.get("title") == name:
                return tool
        
        return None
        
    def execute_tool(self, tool_name: str, action: str) -> Dict[str, Any]:
        """
        Execute a specific action on a tool
        
        Args:
            tool_name: Name of the tool to execute
            action: Action to perform (install, run, etc.)
            
        Returns:
            Dictionary with execution result
        """
        if not self.tools_collection:
            return {"success": False, "message": "No tools collection available"}
            
        tool = self.tools_collection.get_tool_by_name(tool_name)
        if not tool:
            return {"success": False, "message": f"Tool '{tool_name}' not found"}
            
        try:
            if action == "install":
                tool.install()
                return {"success": True, "message": f"Tool '{tool_name}' installed successfully"}
            elif action == "run":
                tool.run()
                return {"success": True, "message": f"Tool '{tool_name}' executed successfully"}
            elif action == "uninstall":
                tool.uninstall()
                return {"success": True, "message": f"Tool '{tool_name}' uninstalled successfully"}
            else:
                return {"success": False, "message": f"Unknown action '{action}'"}
        except Exception as e:
            logger.error(f"Error executing {action} on {tool_name}: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
            
    def export_tools_to_json(self, filepath: str) -> bool:
        """
        Export all tools information to a JSON file
        
        Args:
            filepath: Path to save the JSON file
            
        Returns:
            Boolean indicating success
        """
        try:
            tools = self.get_all_tools()
            with open(filepath, 'w') as f:
                json.dump(tools, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error exporting tools to JSON: {str(e)}")
            return False
            
    def search_tools(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for tools matching the query
        
        Args:
            query: Search query string
            
        Returns:
            List of matching tools
        """
        if not query:
            return []
            
        query = query.lower()
        tools = self.get_all_tools()
        results = []
        
        for tool in tools:
            # Search in title, description, and category
            if (query in tool.get("title", "").lower() or 
                query in tool.get("description", "").lower() or
                query in tool.get("category", "").lower()):
                results.append(tool)
                
        return results