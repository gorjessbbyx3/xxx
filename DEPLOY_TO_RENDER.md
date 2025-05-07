Deploying BINGOxBANGO to Render
This guide will help you deploy the BINGOxBANGO Dark Web Crawler application to Render's free tier.

Prerequisites
A Render account
Your BINGOxBANGO project code in a GitHub repository
Deployment Steps
1. Prepare Your Repository
Make sure your GitHub repository has the following files:

All the project code
dependencies.txt with all dependencies (will be copied to requirements.txt during build)
render.yaml configuration file (created in this project)
2. Deploy to Render
Option 1: Using the Blueprint (Recommended)
Log in to your Render account
Click "New +" and select "Blueprint"
Connect your GitHub repository
Render will automatically detect the render.yaml file and deploy according to the configuration
Option 2: Manual Web Service Setup
Log in to your Render account
Click "New +" and select "Web Service"
Connect your GitHub repository
Configure the service with the following settings:
Name: bingoxbango-dark-web (or any name you prefer)
Environment: Python
Region: Choose the region closest to you
Branch: main (or your default branch)
Build Command: cp dependencies.txt requirements.txt && pip install -r requirements.txt
Start Command: python app.py
Publish Directory: . (root directory)
3. Configure Environment Variables
Add the following environment variables:

PYTHON_VERSION: 3.9.0
PORT: 5000
4. Advanced Configuration
If you need more disk space or other resources, you may need to upgrade from the free tier.

Important Notes for Render Deployment
Limitations on Free Tier
Tor Connectivity: Render's free tier might have limitations regarding Tor connectivity. You may need to modify the application to work without Tor for basic functionality.

Ollama Integration: Ollama service won't be available on Render. Consider these alternatives:

Use OpenAI's API instead (requires API key)
Use another hosted AI service
Disable AI features for the deployed version
Storage Limitations: Free tier has limited storage. Be cautious with crawl results.

Sleep Mode: Free tier services on Render spin down after periods of inactivity. The first request after inactivity will take longer to respond.

Production Considerations
For a production deployment, consider:

Using Render's paid plans for better performance and no sleep mode
Setting up environment variables for any API keys
Implementing proper authentication for the web interface
Configuring database persistence for crawl results
Troubleshooting
If you encounter issues during deployment:

Check Render logs for error messages
Verify all dependencies are properly listed in dependencies.txt
Ensure your start command correctly points to the entry point
Check if any required services (like Tor) are causing issues and adapt accordingly
If you see an error about "Publish directory app/routes.py does not exist", make sure you've set the publishDirectory to "." in render.yaml or in the manual setup
If you see "can't open file '/opt/render/project/src/app/routes.py': [Errno 2] No such file or directory" error, make sure the app.py file is in your repository root - this file handles loading the Flask app properly on Render
Support
For Render-specific issues, refer to Render's documentation or contact their support.

For BINGOxBANGO application issues, refer to the project repository or create an issue on GitHub.

