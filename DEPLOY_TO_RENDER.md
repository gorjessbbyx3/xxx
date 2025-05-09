# Deploying Dark Web Crawler to Render

This guide explains how to deploy the Dark Web Crawler application to Render.

## Prerequisites

1. Your project code in a Git repository
2. The following files in your repository:
   - `requirements.txt`
   - `render.yaml`
   - `Modelfile` (for Ollama/WormGPT)

## Deployment Configuration

The `render.yaml` file is already configured with:

1. Base Python environment
2. Ollama installation and setup
3. Model pulling (mistral:7b)
4. WormGPT model creation
5. Application startup

## Environment Variables

Required environment variables:
- `PYTHON_VERSION`: 3.11.0
- `PORT`: 5000
- `OLLAMA_HOST`: "0.0.0.0"
- `OLLAMA_PORT`: 11434

## Deployment Steps

1. Make sure your code is committed
2. Go to Render dashboard
3. Click "New +" and select "Blueprint"
4. Connect your repository
5. Render will use the `render.yaml` configuration automatically


## Important Notes

1. **AI Integration**: Ollama will be installed and configured during build
2. **First Request**: Initial request may be slow as Ollama loads the model
3. **Resource Usage**: Ensure you have enough resources for running Ollama
4. **Security**: The application includes security tools - use responsibly

## Troubleshooting

If you encounter issues:
1. Check Render logs for errors
2. Verify Ollama is running (`ollama list`)
3. Ensure all dependencies are in requirements.txt
4. Check if models were pulled successfully
5. Check Render logs for error messages
6. Verify all dependencies are properly listed in requirements.txt
7. Ensure your start command correctly points to the entry point
8. Check if any required services (like Tor) are causing issues and adapt accordingly
9. If you see an error about "Publish directory app/routes.py does not exist", make sure you've set the publishDirectory to "." in render.yaml or in the manual setup
10. If you see "can't open file '/opt/render/project/src/app/routes.py': [Errno 2] No such file or directory" error, make sure the app.py file is in your repository root - this file handles loading the Flask app properly on Render

For support, refer to project documentation or create an issue in the repository.