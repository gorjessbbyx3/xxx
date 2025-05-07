"""
Routes for Flask web application
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import os
import logging
import threading
from datetime import datetime
import logging
import threading
import os
import time
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
logger = logging.getLogger('app.routes')

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Global variables to track crawling jobs
crawler_jobs = {}
job_statuses = {}

def check_services():
    """Check the status of required services"""
    # Check Tor
    tor = TorManager()
    tor_status = {
        "running": tor.is_tor_running(),
        "ip": tor.get_current_ip() if tor.is_tor_running() else None
    }

    # Check OpenAI API
    analyzer = OllamaAnalyzer()
    openai_status = {
        "available": analyzer.check_model_availability(),
        "model": analyzer.model_name if analyzer.check_model_availability() else None
    }

    # Get public IP address for location info
    public_ip = tor.get_current_ip() if tor.is_tor_running() else "Unknown"

    return {
        "tor": tor_status,
        "openai": openai_status,
        "public_ip": public_ip
    }

def crawler_thread(job_id, urls, depth, output_dir, analyze_content, max_pages, delay_range):
    """
    Thread function to run the crawler without blocking the web server
    """
    logger.info(f"Starting crawler job {job_id}")
    job_statuses[job_id]["status"] = "running"

    try:
        # Initialize crawler
        crawler = DarkWebCrawler(
            output_dir=output_dir,
            depth=depth,
            delay_range=delay_range,
            analyze_content=analyze_content,
            max_pages=max_pages
        )

        # Start crawling
        result = crawler.start_crawl(urls)

        # Update job status
        job_statuses[job_id].update({
            "status": "completed",
            "end_time": datetime.now().isoformat(),
            "result": result
        })
        logger.info(f"Crawler job {job_id} completed successfully")

    except Exception as e:
        logger.error(f"Error in crawler job {job_id}: {e}")
        job_statuses[job_id].update({
            "status": "failed",
            "end_time": datetime.now().isoformat(),
            "error": str(e)
        })

@app.route('/')
def index():
    """Home page with crawler interface"""
    try:
        service_status = check_services()
    except Exception as e:
        logger.warning(f"Error checking services: {e}")
        service_status = {
            "tor": {"running": False, "ip": None},
            "openai": {"available": False, "model": None},
            "public_ip": "Unknown"
        }
    return render_template('dashboard.html', service_status=service_status, jobs=job_statuses, 
                          now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/chat')
def uncensored_chat():
    """Uncensored chat interface"""
    try:
        service_status = check_services()
    except Exception as e:
        logger.warning(f"Error checking services: {e}")
        service_status = {
            "tor": {"running": False, "ip": None},
            "openai": {"available": False, "model": None},
            "public_ip": "Unknown"
        }
    return render_template('uncensored_chat.html', service_status=service_status)

@app.route('/old')
def old_interface():
    """Old interface"""
    service_status = check_services()
    return render_template('index.html', service_status=service_status, jobs=job_statuses)

@app.route('/crawl', methods=['POST'])
def start_crawl():
    """Start a new crawling job"""
    # Get form data
    urls = request.form.get('urls', '').split('\n')
    urls = [url.strip() for url in urls if url.strip() and is_valid_onion_url(url.strip())]

    if not urls:
        service_status = check_services()
        return render_template('index.html', 
                              service_status=service_status,
                              jobs=job_statuses,
                              error="No valid .onion URLs provided")

    # Get other parameters
    depth = int(request.form.get('depth', 1))
    max_pages = int(request.form.get('max_pages', 50))
    analyze = request.form.get('analyze', 'off') == 'on'

    # Parse delay range
    delay_str = request.form.get('delay', '2-5')
    try:
        min_delay, max_delay = map(float, delay_str.split('-'))
        delay_range = (min_delay, max_delay)
    except ValueError:
        delay_range = (2, 5)

    # Generate job ID and create output directory
    job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir = f"crawl_results/{job_id}"
    create_directory(output_dir)

    # Initialize job status
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

    # Start crawler in a separate thread
    thread = threading.Thread(
        target=crawler_thread,
        args=(job_id, urls, depth, output_dir, analyze, max_pages, delay_range)
    )
    thread.daemon = True
    thread.start()

    # Store thread reference
    crawler_jobs[job_id] = thread

    return redirect(url_for('job_status', job_id=job_id))

@app.route('/status/<job_id>')
def job_status(job_id):
    """Show status of a specific job"""
    if job_id not in job_statuses:
        return redirect(url_for('index'))

    job = job_statuses[job_id]

    # Get list of result files
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
    if job_id in job_statuses:
        return jsonify(job_statuses[job_id])
    else:
        return jsonify({"error": "Job not found"}), 404

@app.route('/api/crawl', methods=['POST'])
def api_crawl():
    """API endpoint to start a new crawling job"""
    data = request.json or {}

    # Get URLs
    urls = data.get('urls', [])
    if isinstance(urls, str):
        urls = [url.strip() for url in urls.split('\n') if url.strip()]

    # Validate URLs
    valid_urls = [url for url in urls if is_valid_onion_url(url)]
    if not valid_urls:
        return jsonify({"error": "No valid .onion URLs provided"}), 400

    # Get other parameters
    depth = int(data.get('depth', 1))
    max_pages = int(data.get('max_pages', 50))
    analyze = data.get('analyze', False)

    # Parse delay range
    delay_str = data.get('delay', '2-5')
    try:
        min_delay, max_delay = map(float, delay_str.split('-'))
        delay_range = (min_delay, max_delay)
    except ValueError:
        delay_range = (2, 5)

    # Generate job ID and create output directory
    job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir = data.get('output_dir', f"crawl_results/{job_id}")
    create_directory(output_dir)

    # Initialize job status
    job_statuses[job_id] = {
        "id": job_id,
        "status": "starting",
        "start_time": datetime.now().isoformat(),
        "urls": valid_urls,
        "depth": depth,
        "max_pages": max_pages,
        "analyze_content": analyze,
        "output_dir": output_dir
    }

    # Start crawler in a separate thread
    thread = threading.Thread(
        target=crawler_thread,
        args=(job_id, valid_urls, depth, output_dir, analyze, max_pages, delay_range)
    )
    thread.daemon = True
    thread.start()

    # Store thread reference
    crawler_jobs[job_id] = thread

    return jsonify({
        "job_id": job_id,
        "status": "starting",
        "status_url": f"/api/jobs/{job_id}"
    })

@app.route('/analyze', methods=['POST'])
def analyze_single():
    """Analyze a single URL without crawling links"""
    url = request.form.get('url', '').strip()

    if not url or not is_valid_onion_url(url):
        service_status = check_services()
        return render_template('index.html', 
                              service_status=service_status,
                              jobs=job_statuses,
                              error="Invalid or missing .onion URL")

    # Generate job ID and create output directory
    job_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir = f"analysis_results/{job_id}"
    create_directory(output_dir)

    # Initialize job status
    job_statuses[job_id] = {
        "id": job_id,
        "status": "starting",
        "start_time": datetime.now().isoformat(),
        "urls": [url],
        "depth": 0,
        "max_pages": 1,
        "analyze_content": True,
        "output_dir": output_dir
    }

    # Start crawler in a separate thread (depth=0 means no link following)
    thread = threading.Thread(
        target=crawler_thread,
        args=(job_id, [url], 0, output_dir, True, 1, (1, 2))
    )
    thread.daemon = True
    thread.start()

    # Store thread reference
    crawler_jobs[job_id] = thread

    return redirect(url_for('job_status', job_id=job_id))

# Security tools section - Hacking Tool Integration
@app.route('/security_tools')
@app.route('/security-tools')  # Keep legacy route for backward compatibility
def security_tools():
    """Security tools dashboard"""
    from security_tools.api import SecurityToolsAPI

    service_status = check_services()
    security_api = SecurityToolsAPI()

    # Get tools organized by category
    tools_by_category = security_api.get_tools_by_category()
    categories = security_api.get_categories()
    total_tools = security_api.get_total_tools_count()

    return render_template('security_tools.html', 
                          service_status=service_status,
                          tools_by_category=tools_by_category,
                          categories=categories,
                          total_tools=total_tools)

@app.route('/search_security_tools')
def search_security_tools():
    """Search security tools"""
    from security_tools.api import SecurityToolsAPI

    query = request.args.get('query', '')
    security_api = SecurityToolsAPI()

    if query:
        results = security_api.search_tools(query)
    else:
        results = []

    return jsonify({"results": results})

@app.route('/tool/<tool_name>')
def view_tool_details(tool_name):
    """View details of a specific security tool"""
    from security_tools.api import SecurityToolsAPI

    security_api = SecurityToolsAPI()
    tool = security_api.get_tool_details(tool_name)

    if not tool:
        return redirect(url_for('security_tools'))

    # Get tool directory
    tool_dir = f"security_tools/tools/{tool_name.lower().replace(' ', '_')}"

    return render_template('tool_details.html', 
                          tool=tool,
                          tool_dir=tool_dir,
                          service_status=check_services())

@app.route('/execute_security_tool/<tool_name>', methods=['POST'])
def execute_security_tool(tool_name):
    """Execute a security tool"""
    from security_tools.api import SecurityToolsAPI

    security_api = SecurityToolsAPI()
    tool = security_api.get_tool_details(tool_name)

    if not tool:
        return jsonify({"error": "Tool not found"}), 404

    # Get tool directory and commands
    tool_dir = f"security_tools/tools/{tool_name.lower().replace(' ', '_')}"
    build_cmd = tool.get('BUILD_COMMAND', '')
    run_cmd = tool.get('RUN_COMMAND', 'python tool.py --help')

    # Create a new workflow for this tool
    workflow_name = f"Run {tool_name}"
    commands = []
    if build_cmd:
        commands.append(f"cd {tool_dir} && {build_cmd}")
    commands.append(f"cd {tool_dir} && {run_cmd}")

    return jsonify({
        "success": True,
        "workflow": workflow_name,
        "commands": commands
    })

@app.route('/custom-tool-generator')
def custom_tool_generator():
    """Custom security tool generator page"""
    return render_template('custom_tool_generator.html',
                          service_status=check_services())

@app.route('/api/generate-tool', methods=['POST'])
def generate_custom_tool():
    """API endpoint to generate a custom security tool"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    description = request.json.get('description')
    if not description:
        return jsonify({"error": "Tool description is required"}), 400

    # In a real implementation, this would use AI to generate the tool
    # For demo, we'll return a placeholder response

    # Simple name generation from description
    words = description.split()
    name_words = [word for word in words if len(word) > 3 and word.lower() not in ['tool', 'that', 'with', 'and', 'for']][:2]
    if not name_words:
        name_words = ['Custom', 'Security']
    if len(name_words) == 1:
        name_words.append('Tool')

    tool_name = ' '.join(word.capitalize() for word in name_words)

    # Simple code generation (placeholder)
    tool_code = f"""#!/usr/bin/env python3
\"\"\"
{tool_name} - Generated by GhostTrace AI

Description:
{description}
\"\"\"

import argparse
import sys
import socket
import random
import time
from datetime import datetime

def print_banner():
    \"\"\"Print the tool banner\"\"\"
    banner = \"\"\"
    ╔═══════════════════════════════════════════════╗
    ║ {tool_name}{' ' * (43 - len(tool_name))} ║
    ║ Generated by GhostTrace AI                     ║
    ╚═══════════════════════════════════════════════╝
    \"\"\"
    print(banner)

def main():
    \"\"\"Main function for the {tool_name} tool\"\"\"
    print_banner()

    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument('-t', '--target', help='Target host or IP address')
    parser.add_argument('-p', '--port', type=int, help='Target port')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    if not args.target:
        parser.print_help()
        sys.exit(1)

    print(f"\\n[*] Starting scan at {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
    print(f"[*] Target: {{args.target}}")

    # Tool implementation would be here
    # This is just a placeholder for demonstration purposes
    print("\\n[*] Running security analysis...")
    for i in range(5):
        time.sleep(0.5)
        print(f"[+] Completed step {{i+1}}/5...")

    print("\\n[+] Scan completed!")
    print("[+] Results:")
    print("    - Finding 1: Example vulnerability detected")
    print("    - Finding 2: Example security issue found")
    print("    - Finding 3: Example recommendation")

if __name__ == "__main__":
    main()
"""

    # In a real implementation, this would save the tool to disk

    return jsonify({
        "success": True,
        "tool_name": tool_name,
        "tool_code": tool_code,
        "message": "Custom tool generated successfully"
    })

@app.route('/interactive-tools')
@app.route('/interactive_tools')  # Add underscore version for compatibility
def interactive_tools():
    """Interactive tools page with vulnerability scanner, location changer, email templates, and bot maker"""
    # Initialize security tools API
    from security_tools.api import SecurityToolsAPI

    service_status = check_services()
    security_api = SecurityToolsAPI()

    return render_template('interactive_tools.html',
                          service_status=service_status)

@app.route('/api/vulnerability-scan', methods=['POST'])
def api_vulnerability_scan():
    """API endpoint to run a vulnerability scan"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    target = request.json.get('target')
    scan_type = request.json.get('scan_type', 'quick')
    use_tor = request.json.get('use_tor', False)
    use_ai = request.json.get('use_ai', True)

    if not target:
        return jsonify({"error": "Target URL or IP is required"}), 400

    # Initialize vulnerability scanner
    from security_tools.vuln_scanner import VulnerabilityScanner

    tor_manager = TorManager() if use_tor else None
    ai_analyzer = OllamaAnalyzer() if use_ai else None

    scanner = VulnerabilityScanner(
        tor_manager=tor_manager,
        ai_analyzer=ai_analyzer
    )

    # Run the scan
    result = scanner.scan_target(target, scan_type=scan_type)

    return jsonify(result)

@app.route('/api/change-location', methods=['POST'])
def api_change_location():
    """API endpoint to change apparent location"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    method = request.json.get('method', 'tor')
    country = request.json.get('country')

    # Initialize location changer
    from security_tools.location_changer import LocationChanger

    tor_manager = TorManager()
    location_changer = LocationChanger(tor_manager=tor_manager)

    # Change location based on method
    if method == 'tor':
        result = location_changer.change_location_tor(country=country)
    elif method == 'proxy':
        result = location_changer.change_location_proxy(country=country)
    elif method == 'vpn':
        result = location_changer.change_location_vpn(country=country)
    else:
        return jsonify({"error": "Invalid method specified"}), 400

    return jsonify(result)

@app.route('/api/current-location')
def api_current_location():
    """API endpoint to get current apparent location"""
    from security_tools.location_changer import LocationChanger

    location_changer = LocationChanger()
    result = location_changer.get_current_location()

    return jsonify(result)

@app.route('/api/email-templates', methods=['GET'])
def api_email_templates():
    """API endpoint to get email templates"""
    category = request.args.get('category')

    from security_tools.email_templates import EmailTemplateManager

    template_manager = EmailTemplateManager()

    if category:
        templates = template_manager.get_templates_by_category(category)
    else:
        # Get all templates grouped by category
        templates = {}
        categories = template_manager.get_template_categories()
        for cat in categories:
            templates[cat] = template_manager.get_templates_by_category(cat)

    return jsonify(templates)

@app.route('/api/email-template/<template_name>', methods=['GET'])
def api_email_template(template_name):
    """API endpoint to get a specific email template"""
    category = request.args.get('category')

    from security_tools.email_templates import EmailTemplateManager

    template_manager = EmailTemplateManager()
    template = template_manager.get_template_by_name(template_name, category)

    if not template:
        return jsonify({"error": "Template not found"}), 404

    return jsonify(template)

@app.route('/api/bot-maker/create', methods=['POST'])
def api_create_bot():
    """API endpoint to create a bot using BotMaker"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    bot_type = request.json.get('bot_type')
    config = request.json.get('config', {})
    use_tor = request.json.get('use_tor', False)

    if not bot_type:
        return jsonify({"error": "Bot type is required"}), 400

    # Initialize bot maker
    try:
        from security_tools.bot_maker import BotMaker
    except ImportError as e:
        logging.error(f"Failed to import BotMaker: {e}")
        return jsonify({"error": "Bot maker module not available"}), 500

    # Initialize required components
    try:
        tor_manager = TorManager() if use_tor else None
        ai_analyzer = OllamaAnalyzer()
    except Exception as e:
        logging.error(f"Failed to initialize components for bot maker: {e}")
        return jsonify({"error": "Failed to initialize components"}), 500

    bot_maker = BotMaker(
        tor_manager=tor_manager,
        ai_analyzer=ai_analyzer
    )

    # Create bot based on type
    try:
        if bot_type == 'web_crawler':
            start_urls = config.get('start_urls', [])
            max_depth = config.get('max_depth', 3)
            max_pages = config.get('max_pages', 50)
            delay_range = config.get('delay_range', (2.0, 5.0))
            keywords = config.get('keywords', [])
            user_agent = config.get('user_agent')

            bot = bot_maker.create_web_crawler_bot(
                start_urls=start_urls,
                max_depth=max_depth,
                max_pages=max_pages,
                delay_range=delay_range,
                keywords=keywords,
                use_tor=use_tor,
                user_agent=user_agent
            )
        elif bot_type == 'network_scanner':
            target = config.get('target', '')
            scan_type = config.get('scan_type', 'port_scan')
            port_range = config.get('port_range')

            bot = bot_maker.create_network_scanner_bot(
                target=target,
                scan_type=scan_type,
                port_range=port_range,
                use_tor=use_tor
            )
        elif bot_type == 'chat_bot':
            platform = config.get('platform', 'discord')
            bot = bot_maker.create_chat_bot(platform, config)
        elif bot_type == 'social_media_bot':
            platform = config.get('platform', 'twitter')
            bot = bot_maker.create_social_media_bot(platform, config)
        elif bot_type == 'crypto_miner_sim':
            network = config.get('network', 'bitcoin')
            bot = bot_maker.create_crypto_miner_bot(network, config)
        else:
            return jsonify({"error": f"Unsupported bot type: {bot_type}"}), 400

        # Start the bot
        bot_maker.start_bot(bot['id'])

        return jsonify(bot)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bot-maker/bots')
def api_list_bots():
    """API endpoint to list all bots"""
    bot_type = request.args.get('type')

    from security_tools.bot_maker import BotMaker

    bot_maker = BotMaker()
    bots = bot_maker.list_bots(bot_type)

    return jsonify(bots)

@app.route('/api/bot-maker/bot/<bot_id>', methods=['GET'])
def api_get_bot(bot_id):
    """API endpoint to get a specific bot's status"""
    from security_tools.bot_maker import BotMaker

    bot_maker = BotMaker()
    status = bot_maker.get_bot_status(bot_id)

    if 'error' in status:
        return jsonify(status), 404

    return jsonify(status)

@app.route('/api/bot-maker/bot/<bot_id>/start', methods=['POST'])
def api_start_bot(bot_id):
    """API endpoint to start a bot"""
    from security_tools.bot_maker import BotMaker

    bot_maker = BotMaker()
    result = bot_maker.start_bot(bot_id)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result)

@app.route('/api/bot-maker/bot/<bot_id>/stop', methods=['POST'])
def api_stop_bot(bot_id):
    """API endpoint to stop a bot"""
    from security_tools.bot_maker import BotMaker

    bot_maker = BotMaker()
    result = bot_maker.stop_bot(bot_id)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result)

@app.route('/api/bot-maker/bot/<bot_id>/delete', methods=['DELETE'])
def api_delete_bot(bot_id):
    """API endpoint to delete a bot"""
    from security_tools.bot_maker import BotMaker

    bot_maker = BotMaker()
    result = bot_maker.delete_bot(bot_id)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result)

@app.route('/api/bot-maker/bot/<bot_id>/task', methods=['POST'])
def api_add_bot_task(bot_id):
    """API endpoint to add a task to a bot"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    task_type = request.json.get('task_type')
    task_data = request.json.get('task_data', {})

    if not task_type:
        return jsonify({"error": "Task type is required"}), 400

    from security_tools.bot_maker import BotMaker

    bot_maker = BotMaker()
    result = bot_maker.add_user_task(bot_id, task_type, task_data)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result)

@app.route('/api/bot-maker/bot/<bot_id>/task/execute', methods=['POST'])
def api_execute_bot_task(bot_id):
    """API endpoint to execute a task for a bot"""
    task_id = request.json.get('task_id') if request.is_json else None

    from security_tools.bot_maker import BotMaker

    bot_maker = BotMaker()
    result = bot_maker.execute_user_task(bot_id, task_id)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result)

@app.route('/check-designer')
def check_designer():
    """Check designer tool with customization options"""
    service_status = check_services()

    # Define standard check dimensions
    check_dimensions = {
        'business': {'width': 8.5, 'height': 3.5},
        'personal': {'width': 6.0, 'height': 2.75},
        'voucher': {'width': 8.5, 'height': 3.67}
    }

    # Define MICR specs
    micr_specs = {
        'font': 'MICR E13-B',
        'size': '0.117 inches',
        'clear_band': {'height': 0.625, 'min_margin': 0.315}
    }

    return render_template('check_designer.html', 
                         service_status=service_status,
                         check_dimensions=check_dimensions,
                         micr_specs=micr_specs)

@app.route('/api/check/validate-micr', methods=['POST'])
def validate_micr():
    """Validate MICR line format"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    routing = request.json.get('routing')
    account = request.json.get('account')
    check_number = request.json.get('check_number')

    # Validate routing number (9 digits)
    if not routing or not routing.isdigit() or len(routing) != 9:
        return jsonify({"error": "Invalid routing number"}), 400

    # Validate account number (usually 8-12 digits)
    if not account or not account.isdigit() or len(account) < 8 or len(account) > 12:
        return jsonify({"error": "Invalid account number"}), 400

    # Validate check number (usually 4 digits)
    if not check_number or not check_number.isdigit():
        return jsonify({"error": "Invalid check number"}), 400

    return jsonify({
        "valid": True,
        "micr_line": f"⑆{routing}⑆ ⑈{account}⑈ {check_number}"
    })

@app.route('/api/save-check-template', methods=['POST'])
def save_check_template():
    """API endpoint to save a check template"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    template_data = request.json.get('template_data')
    template_name = request.json.get('template_name', 'Custom Template')

    if not template_data:
        return jsonify({"error": "Template data is required"}), 400

    # Validate check dimensions
    width = template_data.get('width')
    height = template_data.get('height')

    if width < 6.0 or width > 8.75 or height < 2.75 or height > 3.67:
        return jsonify({"error": "Invalid check dimensions"}), 400

    # Validate MICR line position
    micr_y = template_data.get('micr_position_y', 0)
    if micr_y < (height - 0.625):  # Must be within clear band
        return jsonify({"error": "MICR line must be within clear band"}), 400

    return jsonify({
        "success": True,
        "template_id": str(uuid.uuid4()),
        "name": template_name,
        "message": f"Template '{template_name}' saved successfully"
    })

@app.route('/api/export-check-pdf', methods=['POST'])
def export_check_pdf():
    """API endpoint to export a check design as PDF"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    check_data = request.json.get('check_data')

    if not check_data:
        return jsonify({"error": "Check data is required"}), 400

    # In a production environment, this would generate a PDF
    # For demo purposes, we'll just return success
    return jsonify({
        "success": True,
        "message": "Check PDF exported successfully"
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for uncensored chat with AI"""
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    message = data.get('message')
    uncensored = data.get('uncensored', False)

    # Check OpenAI API status first
    ai_analyzer = OllamaAnalyzer()
    if not ai_analyzer.check_model_availability():
        return jsonify({
            "error": "AI service is currently unavailable. Please try again later.",
            "details": "OpenAI API quota exceeded or invalid key"
        }), 503

    try:
        response = ai_analyzer.get_chat_response(message, uncensored=uncensored)
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error during chat: {e}")
        return jsonify({"error": "An error occurred during the chat. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
