"""
Onion site generator with templates for marketplaces, blogs, and more
"""
import os
import shutil
from typing import Dict, Optional
import jinja2
import secrets
import subprocess

class OnionSiteGenerator:
    """Generate Tor hidden services with various templates"""

    def __init__(self, output_dir: str = "generated_sites"):
        self.output_dir = output_dir
        self.template_loader = jinja2.FileSystemLoader(searchpath="templates/onion_sites")
        self.template_env = jinja2.Environment(loader=self.template_loader)

        # Available templates
        self.templates = {
            "marketplace": {
                "name": "Marketplace",
                "description": "E-commerce platform with product listings and secure messaging",
                "files": ["index.html", "products.html", "messages.html", "style.css"]
            },
            "blog": {
                "name": "Blog Platform",
                "description": "Anonymous blogging platform with markdown support",
                "files": ["index.html", "post.html", "editor.html", "style.css"]
            },
            "forum": {
                "name": "Discussion Forum",
                "description": "Secure discussion forum with categories and threads",
                "files": ["index.html", "topic.html", "profile.html", "style.css"]
            },
            "chat": {
                "name": "Secure Chat",
                "description": "End-to-end encrypted chat platform",
                "files": ["index.html", "chat.html", "style.css"]
            }
        }

    def get_available_templates(self) -> Dict:
        """Get list of available templates"""
        return self.templates

    def generate_site(self, template: str, config: Dict) -> Optional[str]:
        """Generate a new onion site from template"""
        if template not in self.templates:
            return None

        # Create unique site directory
        site_id = secrets.token_hex(8)
        site_dir = os.path.join(self.output_dir, site_id)
        os.makedirs(site_dir, exist_ok=True)

        try:
            # Generate each template file
            for file in self.templates[template]["files"]:
                template_file = f"{template}/{file}"
                output_file = os.path.join(site_dir, file)

                if template_file.endswith((".html", ".css")):
                    try:
                        template_obj = self.template_env.get_template(template_file)
                        content = template_obj.render(**config)
                    except jinja2.exceptions.TemplateNotFound:
                        print(f"Template not found: {template_file}")
                        return None
                    except Exception as e:
                        print(f"Error rendering template: {e}")
                        return None

                    with open(output_file, "w") as f:
                        f.write(content)
                else:
                    # Copy static files
                    shutil.copy2(
                        os.path.join("templates/onion_sites", template_file),
                        output_file
                    )

            return site_id
        except Exception as e:
            print(f"Error generating site: {e}")
            return None

    def configure_tor_service(self, site_id: str, port: int = 5000) -> Optional[str]:
        """Configure Tor hidden service for the site"""
        try:
            # Add hidden service configuration
            config_lines = [
                f"HiddenServiceDir /var/lib/tor/hidden_service_{site_id}/",
                f"HiddenServicePort 80 127.0.0.1:{port}"
            ]

            # In practice, you would modify torrc and restart Tor
            # For demo, just return the config
            return "\n".join(config_lines)
        except Exception as e:
            print(f"Error configuring Tor service: {e}")
            return None

    def deploy_site(self, site_id: str, port: int = 5000) -> bool:
        """Deploy the generated site"""
        try:
            site_dir = os.path.join(self.output_dir, site_id)
            if not os.path.exists(site_dir):
                return False

            # In practice, you would set up a proper web server
            # For demo, use Python's built-in server
            os.chdir(site_dir)
            subprocess.Popen(["python", "-m", "http.server", str(port)])
            return True
        except Exception as e:
            print(f"Error deploying site: {e}")
            return False