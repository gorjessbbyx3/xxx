"""
Routes for Flask web application
"""
from datetime import datetime
import logging
import os
import threading
import uuid
from typing import Dict, List, Any

from flask import (
    Flask, 
    render_template, 
    request, 
    jsonify, 
    redirect, 
    url_for
)

from darkweb_crawler import DarkWebCrawler
from tor_manager import TorManager
from ai_analyzer import OllamaAnalyzer
from utils import create_directory, is_valid_onion_url
from security_tools.api import SecurityToolsAPI
from security_tools.vuln_scanner import VulnerabilityScanner
from security_tools.location_changer import LocationChanger
from security_tools.email_templates import EmailTemplateManager
from security_tools.bot_maker import BotMaker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('app.routes')

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Global variables to track crawling jobs
crawler_jobs = {}
job_statuses = {}

def check_services():
    """Check the status of required services"""
    try:
        # Check Tor
        tor = TorManager()
        tor_status = {
            "running": tor.is_tor_running(),
            "ip": tor.get_current_ip() if tor.is_tor_running() else None
        }

        # Check Ollama
        analyzer = OllamaAnalyzer()
        ollama_status = {
            "available": analyzer.check_model_availability(),
            "model": analyzer.model_name if analyzer.check_model_availability() else None
        }

        # Get public IP address
        public_ip = tor.get_current_ip() if tor.is_tor_running() else "Unknown"

        # Return complete service status
        return {
            "tor": tor_status,
            "ollama": ollama_status,
            "public_ip": public_ip,
            "openai": {
                "available": False,  # Set default OpenAI status
                "model": None
            }
        }
    except Exception as e:
        logger.error(f"Error checking services: {e}")
        return {
            "tor": {"running": False, "ip": None},
            "ollama": {"available": False, "model": None},
            "openai": {"available": False, "model": None},
            "public_ip": "Unknown",
            "error": str(e)
        }

def crawler_thread(job_id: str, urls: List[str], depth: int, output_dir: str, 
                  analyze_content: bool, max_pages: int, delay_range: tuple):
    """Thread function to run the crawler"""
    logger.info(f"Starting crawler job {job_id}")
    job_statuses[job_id]["status"] = "running"

    try:
        crawler = DarkWebCrawler(
            output_dir=output_dir,
            depth=depth,
            delay_range=delay_range,
            analyze_content=analyze_content,
            max_pages=max_pages
        )
        result = crawler.start_crawl(urls)

        job_statuses[job_id].update({
            "status": "completed",
            "end_time": datetime.now().isoformat(),
            "result": result
        })
    except Exception as e:
        logger.error(f"Error in crawler job {job_id}: {e}")
        job_statuses[job_id].update({
            "status": "failed",
            "end_time": datetime.now().isoformat(),
            "error": str(e)
        })

# Route handlers
@app.route('/')
def index():
    """Home page with crawler interface"""
    service_status = check_services()
    return render_template('dashboard.html', 
                         service_status=service_status, 
                         jobs=job_statuses,
                         now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/chat')
def uncensored_chat():
    """Uncensored chat interface"""
    service_status = check_services()
    return render_template('uncensored_chat.html', service_status=service_status)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for uncensored chat with AI"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    message = request.json.get('message')
    if not message:
        return jsonify({"error": "No message provided"}), 400

    uncensored = request.json.get('uncensored', False)
    ai_analyzer = OllamaAnalyzer()

    if not ai_analyzer.check_model_availability():
        return jsonify({
            "error": "AI service unavailable",
            "details": "Ollama service not running"
        }), 503

    try:
        response = ai_analyzer.get_chat_response(message, uncensored=uncensored)
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/crawl', methods=['POST'])
def start_crawl():
    """Start a new crawling job"""
    urls = request.form.get('urls', '').split('\n')
    urls = [url.strip() for url in urls if url.strip() and is_valid_onion_url(url.strip())]

    if not urls:
        service_status = check_services()
        return render_template('index.html',
                             service_status=service_status,
                             jobs=job_statuses,
                             error="No valid .onion URLs provided")

    depth = int(request.form.get('depth', 1))
    max_pages = int(request.form.get('max_pages', 50))
    analyze = request.form.get('analyze', 'off') == 'on'
    delay_str = request.form.get('delay', '2-5')

    try:
        min_delay, max_delay = map(float, delay_str.split('-'))
        delay_range = (min_delay, max_delay)
    except ValueError:
        delay_range = (2, 5)

    job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir = f"crawl_results/{job_id}"
    create_directory(output_dir)

    job_statuses[job_id] = {
        "id": job_id,
        "status": "starting",
        "start_time": datetime.now().isoformat(),
        "urls": urls,
        "depth": depth,
        "max_pages": max_pages,
        "analyze_content": analyze,
        "output_dir": output_dir
    }

    thread = threading.Thread(
        target=crawler_thread,
        args=(job_id, urls, depth, output_dir, analyze, max_pages, delay_range)
    )
    thread.daemon = True
    thread.start()
    crawler_jobs[job_id] = thread

    return redirect(url_for('job_status', job_id=job_id))

@app.route('/status/<job_id>')
def job_status(job_id):
    """Show status of a specific job"""
    if job_id not in job_statuses:
        return redirect(url_for('index'))

    job = job_statuses[job_id]
    result_files = []

    if os.path.exists(job["output_dir"]):
        for root, _, files in os.walk(job["output_dir"]):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, job["output_dir"])
                file_size = os.path.getsize(file_path)
                result_files.append({
                    "name": file,
                    "path": relative_path,
                    "size": file_size
                })

    return render_template('results.html', job=job, files=result_files)

@app.route('/api/status')
def api_status():
    """API endpoint to check service status"""
    return jsonify(check_services())

@app.route('/api/jobs')
def api_jobs():
    """API endpoint to list all jobs"""
    return jsonify(job_statuses)

@app.route('/api/jobs/<job_id>')
def api_job_status(job_id):
    """API endpoint to get status of a specific job"""
    if job_id not in job_statuses:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job_statuses[job_id])

@app.route('/interactive_tools')
def interactive_tools():
    """Interactive tools dashboard"""
    service_status = check_services()
    return render_template('interactive_tools.html', service_status=service_status)

@app.route('/analyze_single', methods=['GET', 'POST'])
def analyze_single():
    """Single URL analysis interface"""
    if request.method == 'POST':
        url = request.form.get('url')
        if url and is_valid_onion_url(url):
            result = analyze_single_url(url)
            return render_template('results.html', 
                                 result=result, 
                                 service_status=check_services())
    return render_template('index.html', 
                         service_status=check_services(),
                         jobs=job_statuses)

@app.route('/security_tools')
@app.route('/security-tools')
def security_tools():
    """Security tools dashboard"""
    security_api = SecurityToolsAPI()
    tools_by_category = security_api.get_tools_by_category()
    categories = security_api.get_categories()
    total_tools = security_api.get_total_tools_count()

    return render_template('security_tools.html',
                         service_status=check_services(),
                         tools_by_category=tools_by_category,
                         categories=categories,
                         total_tools=total_tools)

@app.route('/tool/<tool_name>')
def view_tool_details(tool_name):
    """View details of a specific security tool"""
    security_api = SecurityToolsAPI()
    tool = security_api.get_tool_details(tool_name)

    if not tool:
        return redirect(url_for('security_tools'))

    tool_dir = f"security_tools/tools/{tool_name.lower().replace(' ', '_')}"
    return render_template('tool_details.html',
                         tool=tool,
                         tool_dir=tool_dir,
                         service_status=check_services())

@app.route('/check-designer')
def check_designer():
    """Check designer tool interface"""
    check_dimensions = {
        'business': {'width': 8.5, 'height': 3.5},
        'personal': {'width': 6.0, 'height': 2.75},
        'voucher': {'width': 8.5, 'height': 3.67}
    }

    micr_specs = {
        'font': 'MICR E13-B',
        'size': '0.117 inches',
        'clear_band': {'height': 0.625, 'min_margin': 0.315}
    }

    return render_template('check_designer.html',
                         service_status=check_services(),
                         check_dimensions=check_dimensions,
                         micr_specs=micr_specs)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)