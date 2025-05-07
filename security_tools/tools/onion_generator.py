
"""
Onion Site Generator - Create .onion website templates
"""

import os
import shutil
import logging
from typing import Dict, Optional
import json

logger = logging.getLogger(__name__)

class OnionSiteGenerator:
    """Generate different types of .onion website templates"""
    
    TEMPLATES = {
        "marketplace": {
            "name": "Dark Market Template",
            "description": "A marketplace template with product listings and crypto payments",
            "features": [
                "Product listings", 
                "Shopping cart",
                "Crypto payments",
                "User accounts"
            ]
        },
        "blog": {
            "name": "Anonymous Blog",
            "description": "A minimalist blog template for anonymous publishing",
            "features": [
                "Markdown support",
                "Categories",
                "Comments",
                "RSS feed"
            ]
        },
        "forum": {
            "name": "Hidden Forum",
            "description": "A discussion forum template with user authentication",
            "features": [
                "User registration",
                "Thread categories",
                "Private messaging",
                "Moderation tools"
            ]
        }
    }

    def __init__(self, output_dir: str = "generated_sites"):
        """Initialize the generator"""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def list_templates(self) -> Dict:
        """Get available templates"""
        return self.TEMPLATES

    def generate_site(self, template_type: str, site_name: str, options: Optional[Dict] = None) -> Dict:
        """Generate a new onion site from template"""
        if template_type not in self.TEMPLATES:
            return {"error": f"Template {template_type} not found"}

        try:
            # Create site directory
            site_dir = os.path.join(self.output_dir, site_name)
            if os.path.exists(site_dir):
                return {"error": f"Site {site_name} already exists"}

            os.makedirs(site_dir)

            # Generate the base template
            self._generate_base_template(site_dir, site_name)

            # Add template-specific files
            if template_type == "marketplace":
                self._generate_marketplace(site_dir, options)
            elif template_type == "blog":
                self._generate_blog(site_dir, options)
            elif template_type == "forum":
                self._generate_forum(site_dir, options)

            return {
                "success": True,
                "site_name": site_name,
                "path": site_dir,
                "template": template_type
            }

        except Exception as e:
            logger.error(f"Error generating site: {e}")
            return {"error": str(e)}

    def _generate_base_template(self, site_dir: str, site_name: str):
        """Generate base template files"""
        # Create directories
        os.makedirs(os.path.join(site_dir, "static"))
        os.makedirs(os.path.join(site_dir, "templates"))

        # Create main.py
        with open(os.path.join(site_dir, "main.py"), "w") as f:
            f.write(f'''from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
''')

        # Create base template
        with open(os.path.join(site_dir, "templates", "base.html"), "w") as f:
            f.write(f'''<!DOCTYPE html>
<html>
<head>
    <title>{site_name}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <h1>{site_name}</h1>
        <nav>
            <a href="/">Home</a>
            {% block nav %}{% endblock %}
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; {site_name}</p>
    </footer>
</body>
</html>''')

    def _generate_marketplace(self, site_dir: str, options: Optional[Dict] = None):
        """Generate marketplace template"""
        # Create marketplace-specific templates
        templates_dir = os.path.join(site_dir, "templates")
        
        # Index page
        with open(os.path.join(templates_dir, "index.html"), "w") as f:
            f.write('''{% extends "base.html" %}

{% block nav %}
<a href="/products">Products</a>
<a href="/cart">Cart</a>
<a href="/account">Account</a>
{% endblock %}

{% block content %}
<section class="featured">
    <h2>Featured Products</h2>
    <div class="product-grid">
        <!-- Product listings will go here -->
    </div>
</section>
{% endblock %}''')

        # Add CSS
        with open(os.path.join(site_dir, "static", "style.css"), "w") as f:
            f.write('''/* Dark theme */
body {
    background: #1a1a1a;
    color: #fff;
    font-family: 'Courier New', monospace;
    margin: 0;
    padding: 0;
}

header {
    background: #000;
    padding: 1rem;
}

nav a {
    color: #0f0;
    margin-right: 1rem;
    text-decoration: none;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    padding: 1rem;
}''')

    def _generate_blog(self, site_dir: str, options: Optional[Dict] = None):
        """Generate blog template"""
        templates_dir = os.path.join(site_dir, "templates")
        
        # Index page
        with open(os.path.join(templates_dir, "index.html"), "w") as f:
            f.write('''{% extends "base.html" %}

{% block nav %}
<a href="/archive">Archive</a>
<a href="/categories">Categories</a>
{% endblock %}

{% block content %}
<section class="blog-posts">
    <h2>Latest Posts</h2>
    <div class="post-list">
        <!-- Blog posts will go here -->
    </div>
</section>
{% endblock %}''')

        # Add CSS
        with open(os.path.join(site_dir, "static", "style.css"), "w") as f:
            f.write('''/* Minimalist dark theme */
body {
    background: #111;
    color: #eee;
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
}

header {
    background: #222;
    padding: 1rem;
}

.blog-posts {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}''')

    def _generate_forum(self, site_dir: str, options: Optional[Dict] = None):
        """Generate forum template"""
        templates_dir = os.path.join(site_dir, "templates")
        
        # Index page
        with open(os.path.join(templates_dir, "index.html"), "w") as f:
            f.write('''{% extends "base.html" %}

{% block nav %}
<a href="/categories">Categories</a>
<a href="/members">Members</a>
<a href="/messages">Messages</a>
{% endblock %}

{% block content %}
<section class="forum">
    <h2>Forum Categories</h2>
    <div class="category-list">
        <!-- Forum categories will go here -->
    </div>
</section>
{% endblock %}''')

        # Add CSS
        with open(os.path.join(site_dir, "static", "style.css"), "w") as f:
            f.write('''/* Dark forum theme */
body {
    background: #0a0a0a;
    color: #ccc;
    font-family: 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
}

header {
    background: #151515;
    border-bottom: 1px solid #333;
    padding: 1rem;
}

.forum {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
}''')
