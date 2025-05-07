"""
Main entry point for BINGOxBANGO Dark Web Crawler application.
This file imports and runs the Flask application from app/routes.py.
"""

import os
import sys

# Print current directory for debugging
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")

# Check if app directory exists
if os.path.exists('app'):
    print("app directory exists, checking contents...")
    print(f"app directory contents: {os.listdir('app')}")
else:
    print("Error: 'app' directory not found!")
    sys.exit(1)

# Check for routes.py
if not os.path.exists('app/routes.py'):
    print("Error: 'app/routes.py' not found!")
    sys.exit(1)

# Import the Flask app from app/routes.py
sys.path.insert(0, os.path.abspath('.'))
try:
    from app.routes import app

    if __name__ == '__main__':
        # Create necessary directories
        if not os.path.exists('crawl_results'):
            os.makedirs('crawl_results', exist_ok=True)

        if not os.path.exists(os.path.join('app', 'static', 'generated')):
            os.makedirs(os.path.join('app', 'static', 'generated'), exist_ok=True)

        # Get the PORT from environment variable with a default of 5000
        port = int(os.environ.get('PORT', 5000))

        # Run the Flask app with the host set to 0.0.0.0 to make it externally visible
        app.run(host='0.0.0.0', port=port, debug=True)
except Exception as e:
    print(f"Error importing app: {e}")
    sys.exit(1)
