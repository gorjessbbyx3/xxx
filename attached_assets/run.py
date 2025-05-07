#!/usr/bin/env python3
"""
Run script for GhostTrace Dark Web Crawler
"""
import os
import sys

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes import app

if __name__ == '__main__':
    # Run the web application on 0.0.0.0 to make it accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)