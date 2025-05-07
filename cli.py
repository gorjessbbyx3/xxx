#!/usr/bin/env python3
"""
CLI interface for Dark Web Crawler
"""

import argparse
import json
import logging
from datetime import datetime

from darkweb_crawler import DarkWebCrawler
from tor_manager import TorManager
from ai_analyzer import OllamaAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('cli')

def check_tor_status():
    """Check if Tor is running and display the exit node IP"""
    tor = TorManager()
    if tor.is_tor_running():
        ip = tor.get_current_ip()
        logger.info(f"✅ Tor is running. Current exit node IP: {ip}")
        return True
    else:
        logger.error("❌ Tor is not running. Please start the Tor service.")
        return False

def check_ollama_status():
    """Check if Ollama is running and list available models"""
    analyzer = OllamaAnalyzer()
    if analyzer.wait_for_ollama(max_retries=1, retry_delay=1):
        logger.info("✅ Ollama service is running")
        
        # Try to check model availability
        if analyzer.check_model_availability():
            logger.info(f"✅ Model '{analyzer.model_name}' is available")
        else:
            logger.warning(f"⚠️  Model '{analyzer.model_name}' is not available. Will use fallback model")
        
        return True
    else:
        logger.error("❌ Ollama service is not running")
        return False

def analyze_single_url(url, save_path=None):
    """Analyze a single URL without crawling links"""
    if not check_tor_status() or not check_ollama_status():
        return False
    
    logger.info(f"Analyzing single URL: {url}")
    
    # Create a crawler with depth 0 (no link following)
    crawler = DarkWebCrawler(depth=0, max_pages=1)
    
    # Start crawl with just this URL
    result = crawler.start_crawl([url])
    
    if save_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{save_path}/analysis_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Analysis saved to: {output_file}")
    
    return True

def run_crawler(args):
    """Run the crawler with the specified arguments"""
    if not check_tor_status():
        return False
    
    if not args.no_analysis and not check_ollama_status():
        logger.warning("⚠️  Ollama not available. Disabling content analysis.")
        args.no_analysis = True
    
    # Parse delay range
    try:
        min_delay, max_delay = map(float, args.delay.split('-'))
        delay_range = (min_delay, max_delay)
    except ValueError:
        logger.error("Invalid delay format. Using default 2-5 seconds.")
        delay_range = (2, 5)
    
    # Get starting URLs
    start_urls = []
    
    if args.url:
        start_urls.extend([url.strip() for url in args.url.split(',') if url.strip()])
    
    if args.list_file:
        try:
            with open(args.list_file, 'r') as f:
                for line in f:
                    url = line.strip()
                    if url and not url.startswith('#'):
                        start_urls.append(url)
        except Exception as e:
            logger.error(f"Error reading URL list file: {e}")
    
    # Initialize and start the crawler
    crawler = DarkWebCrawler(
        output_dir=args.output,
        depth=args.depth,
        delay_range=delay_range,
        analyze_content=not args.no_analysis,
        max_pages=args.max_pages
    )
    
    logger.info(f"Starting crawl with {len(start_urls)} URLs...")
    crawler.start_crawl(start_urls)
    return True

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='GhostTrace Dark Web Crawler and Analyzer')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Check status command
    status_parser = subparsers.add_parser('status', help='Check the status of required services')
    
    # Crawl command
    crawl_parser = subparsers.add_parser('crawl', help='Crawl dark web URLs')
    crawl_parser.add_argument('--url', '-u', help='Starting URL(s) for crawling (comma-separated)')
    crawl_parser.add_argument('--depth', '-d', type=int, default=1, help='Maximum crawl depth')
    crawl_parser.add_argument('--output', '-o', default='crawl_results', help='Output directory')
    crawl_parser.add_argument('--max-pages', '-m', type=int, default=50, help='Maximum number of pages to crawl')
    crawl_parser.add_argument('--no-analysis', action='store_true', help='Disable AI content analysis')
    crawl_parser.add_argument('--delay', type=str, default='2-5', help='Delay range between requests (format: min-max)')
    crawl_parser.add_argument('--list-file', '-f', help='File containing list of URLs to crawl')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a single dark web URL')
    analyze_parser.add_argument('url', help='URL to analyze')
    analyze_parser.add_argument('--output', '-o', default='analysis_results', help='Output directory')
    
    args = parser.parse_args()
    
    # Process commands
    if args.command == 'status':
        check_tor_status()
        check_ollama_status()
    elif args.command == 'crawl':
        run_crawler(args)
    elif args.command == 'analyze':
        analyze_single_url(args.url, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
