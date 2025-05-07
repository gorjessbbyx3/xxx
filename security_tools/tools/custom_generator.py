"""
Custom Tool Generator - AI-powered security tool creation
"""

from security_tools.core import HackingTool, HackingToolsCollection
import logging
import os
import json
import subprocess
import tempfile
import datetime

# Set up logging
logger = logging.getLogger(__name__)

class CustomToolGeneratorTool(HackingTool):
    TITLE = "Custom Tool Generator"
    DESCRIPTION = "AI-powered tool that creates custom security tools based on your requirements"
    CATEGORY = "Custom Tools"
    PROJECT_URL = ""
    
    def __init__(self):
        super().__init__(options=[
            ("Generate New Tool", self.generate_tool),
            ("View My Tools", self.view_tools)
        ])
        self.tools_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "user_tools")
        
        # Create user tools directory if it doesn't exist
        if not os.path.exists(self.tools_dir):
            os.makedirs(self.tools_dir, exist_ok=True)
    
    def generate_tool(self):
        """Generate a custom security tool based on user input"""
        print("\n🛠️ Custom Security Tool Generator 🛠️")
        print("-------------------------------------")
        print("This tool uses AI to create custom security tools based on your specifications.")
        print("Describe what you need, and the AI will generate a Python script for you.")
        print("\nExample requests:")
        print(" - A port scanner that checks for common vulnerabilities")
        print(" - A password strength analyzer with recommendations")
        print(" - A tool to detect SQL injection vulnerabilities in a website")
        
        description = input("\nDescribe the security tool you need: ")
        
        if not description:
            print("You must provide a description of the tool you need.")
            return
        
        print("\nGenerating your custom security tool...")
        print("This might take a minute...")
        
        # In a real implementation, this would call an LLM API
        # For now, we'll create a simple template tool
        
        # Create a simple name for the tool based on the description
        tool_name = "_".join(description.lower().split()[:3])
        tool_name = ''.join(c if c.isalnum() or c == '_' else '' for c in tool_name)
        
        # Current timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        tool_filename = f"{tool_name}_{timestamp}.py"
        
        # Create the tool file
        tool_path = os.path.join(self.tools_dir, tool_filename)
        
        with open(tool_path, 'w') as f:
            f.write(self._generate_tool_code(tool_name, description))
        
        print(f"\n✅ Your custom tool has been created!")
        print(f"📂 Tool saved as: {tool_path}")
        print(f"💻 To run your tool: python {tool_path}")
        
        return tool_path
    
    def view_tools(self):
        """View previously generated custom tools"""
        print("\n📋 Your Custom Security Tools 📋")
        print("-------------------------------")
        
        if not os.path.exists(self.tools_dir):
            print("No custom tools directory found.")
            return
        
        tools = [f for f in os.listdir(self.tools_dir) if f.endswith('.py')]
        
        if not tools:
            print("You haven't created any custom tools yet.")
            return
        
        print(f"Found {len(tools)} custom tools:\n")
        
        for i, tool in enumerate(tools, 1):
            # Extract the tool name from the filename
            tool_name = tool.rsplit('_', 2)[0].replace('_', ' ').title()
            tool_path = os.path.join(self.tools_dir, tool)
            tool_size = os.path.getsize(tool_path)
            tool_date = datetime.datetime.fromtimestamp(os.path.getctime(tool_path)).strftime("%Y-%m-%d %H:%M")
            
            print(f"{i}. {tool_name}")
            print(f"   File: {tool}")
            print(f"   Created: {tool_date}")
            print(f"   Size: {tool_size} bytes")
            print()
        
        tool_choice = input("\nEnter tool number to view (or 0 to return): ")
        
        try:
            tool_choice = int(tool_choice)
            if tool_choice == 0:
                return
            
            if 1 <= tool_choice <= len(tools):
                selected_tool = tools[tool_choice - 1]
                tool_path = os.path.join(self.tools_dir, selected_tool)
                
                print(f"\n📜 Viewing tool: {selected_tool}\n")
                
                with open(tool_path, 'r') as f:
                    print(f.read())
                
                action = input("\nWhat would you like to do with this tool? (r)un, (d)elete, (b)ack: ")
                
                if action.lower() == 'r':
                    print(f"\nRunning {selected_tool}...")
                    # In a real implementation, we would run the tool safely
                    print("Tool execution not implemented in this demo.")
                elif action.lower() == 'd':
                    confirm = input(f"Are you sure you want to delete {selected_tool}? (y/n): ")
                    if confirm.lower() == 'y':
                        os.remove(tool_path)
                        print(f"\n✅ {selected_tool} has been deleted.")
                
            else:
                print("Invalid tool number.")
        except ValueError:
            print("Please enter a number.")
    
    def _generate_tool_code(self, tool_name, description):
        """Generate Python code for the custom tool based on description"""
        # This is a simple template - in a real implementation, this would call an LLM API
        template = f'''#!/usr/bin/env python3
"""
{description.title()}

This tool was automatically generated by the GhostTrace Custom Tool Generator.
"""

import argparse
import sys
import socket
import random
import time
from datetime import datetime

def print_banner():
    """Print the tool banner"""
    banner = """
    ╔═══════════════════════════════════════════════╗
    ║ GhostTrace Custom Security Tool                ║
    ║ {description[:40] + '...' if len(description) > 40 else description.ljust(40)} ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main function for the {tool_name} tool"""
    print_banner()
    
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument('-t', '--target', help='Target host or IP address')
    parser.add_argument('-p', '--port', type=int, help='Target port')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    if not args.target:
        parser.print_help()
        sys.exit(1)
    
    print(f"\\n[*] Starting scan at {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
    print(f"[*] Target: {{args.target}}")
    
    # Placeholder for actual tool functionality
    # This would be generated based on the user's requirements
    print("\\n[*] This is a placeholder for your custom tool functionality")
    print("[*] In a real implementation, this would be a fully functional tool")
    print("[*] based on your description: {description}")
    
    # Simulate some work
    print("\\n[*] Running analysis...")
    for i in range(5):
        time.sleep(0.5)
        print(f"[+] Completed step {{i+1}}/5...")
    
    print("\\n[+] Scan completed successfully!")
    print("[+] Example results:")
    print("    - Finding 1: Example vulnerability detected")
    print("    - Finding 2: Example security issue found")
    print("    - Finding 3: Example recommendation")
    
    print("\\n[*] For a fully functional tool matching your requirements,")
    print("[*] please use the complete version of the Custom Tool Generator.")

if __name__ == "__main__":
    main()
'''
        return template


class CustomToolsCollection(HackingToolsCollection):
    TITLE = "Custom Tools"
    DESCRIPTION = "Create and manage your own custom security tools"
    
    TOOLS = [
        CustomToolGeneratorTool()
    ]