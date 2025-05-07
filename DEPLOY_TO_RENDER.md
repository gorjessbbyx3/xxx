# Deploying BINGOxBANGO to Render

This guide will help you deploy the BINGOxBANGO Dark Web Crawler application to Render's free tier.

## Prerequisites

1. A [Render](https://render.com/) account
2. Your BINGOxBANGO project code in a GitHub repository

## Deployment Steps

### 1. Prepare Your Repository

Make sure your GitHub repository has the following files:
- All the project code
- `dependencies.txt` with all dependencies (will be copied to requirements.txt during build)
- `render.yaml` configuration file (created in this project)

### 2. Deploy to Render

#### Option 1: Using the Blueprint (Recommended)

1. Log in to your Render account
2. Click "New +" and select "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file and deploy according to the configuration

#### Option 2: Manual Web Service Setup

1. Log in to your Render account
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service with the following settings:

- **Name**: bingoxbango-dark-web (or any name you prefer)
- **Environment**: Python
- **Region**: Choose the region closest to you
- **Branch**: main (or your default branch)
- **Build Command**: `cp dependencies.txt requirements.txt && pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Publish Directory**: `.` (root directory)

### 3. Configure Environment Variables

Add the following environment variables:
- `PYTHON_VERSION`: 3.9.0
- `PORT`: 5000

### 4. Advanced Configuration

If you need more disk space or other resources, you may need to upgrade from the free tier.

## Important Notes for Render Deployment

### Limitations on Free Tier

1. **Tor Connectivity**: Render's free tier might have limitations regarding Tor connectivity. You may need to modify the application to work without Tor for basic functionality.

2. **Ollama Integration**: Ollama service won't be available on Render. Consider these alternatives:
   - Use OpenAI's API instead (requires API key)
   - Use another hosted AI service
   - Disable AI features for the deployed version

3. **Storage Limitations**: Free tier has limited storage. Be cautious with crawl results.

4. **Sleep Mode**: Free tier services on Render spin down after periods of inactivity. The first request after inactivity will take longer to respond.

### Production Considerations

For a production deployment, consider:

1. Using Render's paid plans for better performance and no sleep mode
2. Setting up environment variables for any API keys
3. Implementing proper authentication for the web interface
4. Configuring database persistence for crawl results

## Troubleshooting

If you encounter issues during deployment:

1. Check Render logs for error messages
2. Verify all dependencies are properly listed in dependencies.txt
3. Ensure your start command correctly points to the entry point
4. Check if any required services (like Tor) are causing issues and adapt accordingly
5. If you see an error about "Publish directory app/routes.py does not exist", make sure you've set the publishDirectory to "." in render.yaml or in the manual setup
6. If you see "can't open file '/opt/render/project/src/app/routes.py': [Errno 2] No such file or directory" error, make sure the app.py file is in your repository root - this file handles loading the Flask app properly on Render

## Support

For Render-specific issues, refer to [Render's documentation](https://render.com/docs) or contact their support.

For BINGOxBANGO application issues, refer to the project repository or create an issue on GitHub.