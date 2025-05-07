"""
Web API for Dark Web Crawler - Provides HTTP API for controlling the crawler
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import logging
import os
import threading
from datetime import datetime

from darkweb_crawler import DarkWebCrawler
from tor_manager import TorManager
from ai_analyzer import OllamaAnalyzer
from utils import create_directory, is_valid_onion_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('web_api')

app = Flask(__name__)

# Global variables
crawler_threads = {}
crawler_results = {}

def get_tor_status():
    """Get Tor connection status"""
    tor = TorManager()
    if tor.is_tor_running():
        return {
            "status": "running",
            "exit_node_ip": tor.get_current_ip()
        }
    else:
        return {
            "status": "not_running"
        }

def get_ollama_status():
    """Get Ollama service status"""
    analyzer = OllamaAnalyzer()
    if analyzer.wait_for_ollama(max_retries=1, retry_delay=1):
        model_available = analyzer.check_model_availability()
        return {
            "status": "running",
            "model": analyzer.model_name,
            "model_available": model_available
        }
    else:
        return {
            "status": "not_running"
        }

def start_crawler_thread(job_id, urls, depth, output_dir, analyze, max_pages, delay_range):
    """Start a crawler in a separate thread"""
    logger.info(f"Starting crawler job {job_id} with {len(urls)} URLs")
    
    # Create a new crawler instance
    crawler = DarkWebCrawler(
        output_dir=output_dir,
        depth=depth,
        delay_range=delay_range,
        analyze_content=analyze,
        max_pages=max_pages
    )
    
    # Start the crawl
    try:
        result = crawler.start_crawl(urls)
        crawler_results[job_id] = {
            "status": "completed",
            "result": result,
            "completed_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in crawler job {job_id}: {e}")
        crawler_results[job_id] = {
            "status": "failed",
            "error": str(e),
            "completed_at": datetime.now().isoformat()
        }

@app.route('/')
def index():
    """Render the main page"""
    tor_status = get_tor_status()
    ollama_status = get_ollama_status()
    
    return render_template('index.html', 
                          tor_status=tor_status, 
                          ollama_status=ollama_status,
                          crawler_jobs=crawler_results)

@app.route('/api/status')
def api_status():
    """API endpoint to get the status of services"""
    return jsonify({
        "tor": get_tor_status(),
        "ollama": get_ollama_status(),
        "active_jobs": len([job for job, details in crawler_results.items() 
                           if details.get("status") == "running"]),
        "completed_jobs": len([job for job, details in crawler_results.items() 
                            if details.get("status") in ["completed", "failed"]])
    })

@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """API endpoint to list all crawler jobs"""
    return jsonify(crawler_results)

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    """API endpoint to get details of a specific job"""
    if job_id in crawler_results:
        return jsonify(crawler_results[job_id])
    else:
        return jsonify({"error": "Job not found"}), 404

@app.route('/api/jobs/<job_id>/cancel', methods=['POST'])
def cancel_job(job_id):
    """API endpoint to cancel a running job"""
    if job_id in crawler_threads:
        # We can't actually stop the thread safely, but we can mark it as cancelled
        crawler_results[job_id]["status"] = "cancelled"
        return jsonify({"message": f"Job {job_id} marked for cancellation"})
    else:
        return jsonify({"error": "Job not found or already completed"}), 404

@app.route('/api/crawl', methods=['POST'])
def start_crawl():
    """API endpoint to start a new crawler job"""
    data = request.json or {}
    
    # Generate a job ID
    job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Get parameters
    urls = data.get('urls', [])
    if isinstance(urls, str):
        urls = [url.strip() for url in urls.split(',') if url.strip()]
    
    # Validate URLs
    valid_urls = [url for url in urls if is_valid_onion_url(url)]
    if not valid_urls:
        return jsonify({
            "error": "No valid .onion URLs provided", 
            "invalid_urls": [url for url in urls if url not in valid_urls]
        }), 400
    
    depth = int(data.get('depth', 1))
    output_dir = data.get('output_dir', f'crawl_results/{job_id}')
    analyze = data.get('analyze', True)
    max_pages = int(data.get('max_pages', 50))
    
    # Parse delay range
    delay_str = data.get('delay', '2-5')
    try:
        min_delay, max_delay = map(float, delay_str.split('-'))
        delay_range = (min_delay, max_delay)
    except ValueError:
        delay_range = (2, 5)
    
    # Create output directory
    create_directory(output_dir)
    
    # Initialize job status
    crawler_results[job_id] = {
        "id": job_id,
        "status": "running",
        "created_at": datetime.now().isoformat(),
        "parameters": {
            "urls": valid_urls,
            "depth": depth,
            "output_dir": output_dir,
            "analyze": analyze,
            "max_pages": max_pages,
            "delay_range": delay_range
        }
    }
    
    # Start crawler in a thread
    thread = threading.Thread(
        target=start_crawler_thread,
        args=(job_id, valid_urls, depth, output_dir, analyze, max_pages, delay_range)
    )
    thread.daemon = True
    thread.start()
    
    crawler_threads[job_id] = thread
    
    return jsonify({
        "job_id": job_id,
        "message": f"Crawler job started with {len(valid_urls)} URLs",
        "status_url": f"/api/jobs/{job_id}"
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_url():
    """API endpoint to analyze a single URL"""
    data = request.json or {}
    url = data.get('url')
    
    if not url or not is_valid_onion_url(url):
        return jsonify({"error": "Invalid or missing .onion URL"}), 400
    
    # Generate a job ID
    job_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir = data.get('output_dir', f'analysis_results/{job_id}')
    
    # Create a crawler with depth 0 (no link following)
    crawler = DarkWebCrawler(
        output_dir=output_dir,
        depth=0,
        max_pages=1,
        analyze_content=True
    )
    
    # Initialize job status
    crawler_results[job_id] = {
        "id": job_id,
        "status": "running",
        "created_at": datetime.now().isoformat(),
        "parameters": {
            "url": url,
            "output_dir": output_dir
        }
    }
    
    # Start crawler in a thread for the single URL
    thread = threading.Thread(
        target=start_crawler_thread,
        args=(job_id, [url], 0, output_dir, True, 1, (1, 2))
    )
    thread.daemon = True
    thread.start()
    
    crawler_threads[job_id] = thread
    
    return jsonify({
        "job_id": job_id,
        "message": f"Analysis started for URL: {url}",
        "status_url": f"/api/jobs/{job_id}"
    })

@app.route('/start_crawl', methods=['POST'])
def web_start_crawl():
    """Web form endpoint to start a new crawler job"""
    urls = request.form.get('urls', '')
    depth = int(request.form.get('depth', 1))
    max_pages = int(request.form.get('max_pages', 50))
    analyze = request.form.get('analyze', 'on') == 'on'
    
    # Call the API endpoint
    api_response = start_crawl()
    job_id = api_response.json.get('job_id')
    
    return redirect(url_for('index'))

@app.route('/results/<job_id>')
def show_results(job_id):
    """Show results of a specific job"""
    if job_id not in crawler_results:
        return render_template('results.html', error="Job not found")
    
    job_data = crawler_results[job_id]
    output_dir = job_data.get('parameters', {}).get('output_dir')
    
    # List available result files
    files = []
    if output_dir and os.path.exists(output_dir):
        for root, dirs, filenames in os.walk(output_dir):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, output_dir)
                
                # Get file details
                stats = os.stat(file_path)
                size = stats.st_size
                mod_time = datetime.fromtimestamp(stats.st_mtime)
                
                files.append({
                    'name': filename,
                    'path': rel_path,
                    'size': size,
                    'modified': mod_time
                })
    
    return render_template('results.html', job=job_data, files=files)

def start_api_server():
    """Start the Flask API server"""
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    start_api_server()
