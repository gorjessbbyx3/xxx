
"""
Main entry point for Dark Web Crawler application.
"""
import os
from app.routes import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Configure app settings
    app.config['HOST'] = host
    app.config['PORT'] = port
    app.config['OLLAMA_HOST'] = os.environ.get('OLLAMA_HOST', '0.0.0.0')
    app.config['OLLAMA_PORT'] = int(os.environ.get('OLLAMA_PORT', 11434))
    
    # Run the application
    app.run(host=host, port=port)
