#!/usr/bin/env python3
"""
Dark Web Crawler - A tool for crawling and analyzing dark web content
"""

import argparse
import logging
import os
import time
import re
import json
import random
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests

from tor_manager import TorManager, tor_session_context
from ai_analyzer import OllamaAnalyzer
from utils import sanitize_filename, create_directory, is_valid_onion_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('darkweb_crawler')

class DarkWebCrawler:
    """
    Crawler for accessing and analyzing dark web content
    """
    def __init__(
        self, 
        output_dir='crawl_results', 
        depth=1, 
        delay_range=(2, 5),
        analyze_content=True,
        max_pages=50
    ):
        """
        Initialize the dark web crawler with specified parameters
        
        Args:
            output_dir: Directory to store crawl results
            depth: Maximum crawl depth
            delay_range: Random delay range between requests (seconds)
            analyze_content: Whether to analyze content with AI
            max_pages: Maximum number of pages to crawl
        """
        self.output_dir = output_dir
        self.depth = depth
        self.delay_range = delay_range
        self.analyze_content = analyze_content
        self.max_pages = max_pages
        self.visited_urls = set()
        self.page_count = 0
        
        # Create output directory if it doesn't exist
        create_directory(output_dir)
        
        # Initialize AI analyzer if needed
        if analyze_content:
            self.analyzer = OllamaAnalyzer()
            if not self.analyzer.wait_for_ollama():
                logger.warning("Ollama service not available. Content analysis will be disabled.")
                self.analyze_content = False
    
    def extract_links(self, soup, base_url):
        """
        Extract all links from a BeautifulSoup object
        
        Args:
            soup: BeautifulSoup object of the page
            base_url: Base URL for resolving relative links
            
        Returns:
            List of absolute URLs found on the page
        """
        links = []
        for anchor in soup.find_all('a', href=True):
            href = anchor['href'].strip()
            if href and not href.startswith(('#', 'javascript:', 'mailto:')):
                absolute_url = urljoin(base_url, href)
                # Only include .onion URLs
                if is_valid_onion_url(absolute_url):
                    links.append(absolute_url)
        return links
    
    def save_page(self, url, content, soup=None, analysis=None):
        """
        Save the crawled page and its analysis
        
        Args:
            url: URL of the page
            content: Raw HTML content
            soup: BeautifulSoup object (optional)
            analysis: AI analysis results (optional)
            
        Returns:
            Path to the saved file
        """
        # Create a directory for this domain
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        domain_dir = os.path.join(self.output_dir, sanitize_filename(domain))
        create_directory(domain_dir)
        
        # Generate a filename based on the URL and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = sanitize_filename(f"{parsed_url.path or 'index'}_{timestamp}")
        
        # Save the raw HTML
        html_path = os.path.join(domain_dir, f"{filename_base}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Extract and save the text content
        if soup is not None:
            text_content = self.extract_text_content(soup)
            text_path = os.path.join(domain_dir, f"{filename_base}.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
        
        # Save the analysis if available
        if analysis is not None:
            analysis_path = os.path.join(domain_dir, f"{filename_base}_analysis.json")
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2)
        
        logger.info(f"Saved page from {url} to {html_path}")
        return html_path
    
    def extract_text_content(self, soup):
        """
        Extract readable text content from a BeautifulSoup object
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Extracted text content
        """
        # Remove script and style elements
        for script_or_style in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
            script_or_style.decompose()
        
        # Get text and remove extra whitespace
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def analyze_page(self, url, html_content, soup):
        """
        Analyze the page content using the AI model
        
        Args:
            url: URL of the page
            html_content: Raw HTML content
            soup: BeautifulSoup object
            
        Returns:
            Analysis results dictionary
        """
        if not self.analyze_content:
            return None
        
        try:
            # Extract text content for analysis
            text_content = self.extract_text_content(soup)
            
            if not text_content.strip():
                logger.warning(f"No text content found at {url}")
                return {
                    "url": url,
                    "error": "No text content found",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Get basic content analysis
            analysis_result = self.analyzer.analyze_content(text_content)
            
            # Get entity extraction
            entities = self.analyzer.extract_entities(text_content)
            
            # Get content categorization
            categorization = self.analyzer.categorize_content(text_content)
            
            # Combine all analysis results
            result = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "general_analysis": analysis_result.get("analysis", ""),
                "entities": entities,
                "categorization": categorization,
                "text_length": len(text_content)
            }
            
            logger.info(f"Completed analysis for {url}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing content from {url}: {e}")
            return {
                "url": url,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def crawl_url(self, tor_session, url, current_depth=0):
        """
        Crawl a single URL and its linked pages up to the specified depth
        
        Args:
            tor_session: TorManager instance
            url: URL to crawl
            current_depth: Current crawl depth
            
        Returns:
            List of links found
        """
        if current_depth > self.depth or url in self.visited_urls or self.page_count >= self.max_pages:
            return []
        
        logger.info(f"Crawling: {url} (depth: {current_depth}/{self.depth})")
        self.visited_urls.add(url)
        self.page_count += 1
        
        try:
            # Add random delay to avoid detection
            delay = random.uniform(self.delay_range[0], self.delay_range[1])
            time.sleep(delay)
            
            # Request the page through Tor
            response = tor_session.get(url)
            
            if response.status_code != 200:
                logger.warning(f"Failed to fetch {url}: Status code {response.status_code}")
                return []
            
            # Parse the content
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Analyze the content if enabled
            analysis = self.analyze_page(url, html_content, soup) if self.analyze_content else None
            
            # Save the page
            self.save_page(url, html_content, soup, analysis)
            
            # Extract links for further crawling
            links = self.extract_links(soup, url)
            logger.info(f"Found {len(links)} links on {url}")
            
            # Crawl the found links if not at max depth
            if current_depth < self.depth:
                for link in links:
                    if link not in self.visited_urls and self.page_count < self.max_pages:
                        self.crawl_url(tor_session, link, current_depth + 1)
            
            return links
            
        except RequestException as e:
            logger.error(f"Error crawling {url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error crawling {url}: {e}")
            return []
    
    def start_crawl(self, start_urls):
        """
        Start the crawling process from the given URLs
        
        Args:
            start_urls: List of URLs to start crawling from
            
        Returns:
            Dictionary with crawl results
        """
        start_time = time.time()
        results = {
            "start_time": datetime.now().isoformat(),
            "crawled_pages": 0,
            "visited_urls": []
        }
        
        try:
            # Use the Tor context manager
            with tor_session_context() as tor:
                logger.info(f"Starting crawl with {len(start_urls)} seed URLs")
                
                for url in start_urls:
                    if is_valid_onion_url(url):
                        self.crawl_url(tor, url)
                    else:
                        logger.warning(f"Skipping invalid onion URL: {url}")
                
                results["crawled_pages"] = self.page_count
                results["visited_urls"] = list(self.visited_urls)
                
        except Exception as e:
            logger.error(f"Error in crawl process: {e}")
            results["error"] = str(e)
        
        end_time = time.time()
        results["duration_seconds"] = end_time - start_time
        results["end_time"] = datetime.now().isoformat()
        
        # Save crawl summary
        summary_path = os.path.join(self.output_dir, f"crawl_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(summary_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Crawl completed. Visited {self.page_count} pages in {results['duration_seconds']:.2f} seconds")
        return results


def main():
    """
    Main function to run the dark web crawler
    """
    parser = argparse.ArgumentParser(description='Dark Web Crawler with AI Analysis')
    parser.add_argument('--url', '-u', help='Starting URL(s) for crawling (comma-separated)', required=False)
    parser.add_argument('--depth', '-d', type=int, default=1, help='Maximum crawl depth')
    parser.add_argument('--output', '-o', default='crawl_results', help='Output directory')
    parser.add_argument('--max-pages', '-m', type=int, default=50, help='Maximum number of pages to crawl')
    parser.add_argument('--no-analysis', action='store_true', help='Disable AI content analysis')
    parser.add_argument('--delay', type=str, default='2-5', help='Delay range between requests (format: min-max)')
    parser.add_argument('--list-file', '-f', help='File containing list of URLs to crawl')
    
    args = parser.parse_args()
    
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
    
    # If no URLs provided, use some default .onion directories
    if not start_urls:
        logger.info("No URLs provided. Using default onion directories.")
        start_urls = [
            "http://darkfailllnkf4vf.onion/",  # Dark.fail
            "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page",  # Hidden Wiki
            "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/"  # Ahmia search
        ]
    
    # Initialize and start the crawler
    crawler = DarkWebCrawler(
        output_dir=args.output,
        depth=args.depth,
        delay_range=delay_range,
        analyze_content=not args.no_analysis,
        max_pages=args.max_pages
    )
    
    crawler.start_crawl(start_urls)


if __name__ == "__main__":
    main()
