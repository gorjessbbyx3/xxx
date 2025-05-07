Deploying Dark Web Crawler to Render
This guide explains how to deploy the Dark Web Crawler application to Render.

Prerequisites
Your project code in a Git repository
The following files in your repository:
requirements.txt
render.yaml
Modelfile (for Ollama/WormGPT)
Deployment Configuration
The render.yaml file is already configured with:

Base Python environment
Ollama installation and setup
Model pulling (mistral:7b)
WormGPT model creation
Application startup
Environment Variables
Required environment variables:

PYTHON_VERSION: 3.11.0
PORT: 5000
OLLAMA_HOST: "0.0.0.0"
OLLAMA_PORT: 11434
Deployment Steps
Make sure your code is committed
Go to Render dashboard
Click "New +" and select "Blueprint"
Connect your repository
Render will use the render.yaml configuration automatically
Important Notes
AI Integration: Ollama will be installed and configured during build
First Request: Initial request may be slow as Ollama loads the model
Resource Usage: Ensure you have enough resources for running Ollama
Security: The application includes security tools - use responsibly
Troubleshooting
If you encounter issues:

Check Render logs for errors
Verify Ollama is running (ollama list)
Ensure all dependencies are in requirements.txt
Check if models were pulled successfully
Check Render logs for error messages
Verify all dependencies are properly listed in requirements.txt
Ensure your start command correctly points to the entry point
Check if any required services (like Tor) are causing issues and adapt accordingly
If you see an error about "Publish directory app/routes.py does not exist", make sure you've set the publishDirectory to "." in render.yaml or in the manual setup
If you see "can't open file '/opt/render/project/src/app/routes.py': [Errno 2] No such file or directory" error, make sure the app.py file is in your repository root - this file handles loading the Flask app properly on Render
For support, refer to project documentation or create an issue in the repository.
