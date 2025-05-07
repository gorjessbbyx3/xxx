
#!/usr/bin/env python3
"""
Dark Web Crawler - A tool for crawling and analyzing dark web content with enhanced features
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
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pdfkit
import requests
from difflib import SequenceMatcher
from collections import defaultdict

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
    """Enhanced crawler with new security and analysis features"""
    
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
    ]

    def __init__(self, output_dir='crawl_results', depth=1, delay_range=(2, 5),
                 analyze_content=True, max_pages=50, capture_screenshots=False,
                 export_pdf=False, rotate_user_agent=True, custom_cookies=None,
                 respect_robots=True):
        """Initialize crawler with enhanced features"""
        self.output_dir = output_dir
        self.depth = depth
        self.delay_range = delay_range
        self.analyze_content = analyze_content
        self.max_pages = max_pages
        self.capture_screenshots = capture_screenshots
        self.export_pdf = export_pdf
        self.rotate_user_agent = rotate_user_agent
        self.custom_cookies = custom_cookies or {}
        self.respect_robots = respect_robots
        self.visited_urls = set()
        self.page_count = 0
        self.text_content_cache = defaultdict(str)
        self.current_user_agent_idx = 0
        self.cookie_jar = {}
        self.robots_cache = {}

        # Create output directory
        create_directory(output_dir)

        # Initialize AI analyzer
        if analyze_content:
            self.analyzer = OllamaAnalyzer()
            if not self.analyzer.wait_for_ollama():
                logger.warning("Ollama service not available. Content analysis will be disabled.")
                self.analyze_content = False

        # Initialize Selenium for screenshots if needed
        if capture_screenshots:
            self.init_selenium()

    def init_selenium(self):
        """Initialize Selenium WebDriver for screenshots"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            self.driver = webdriver.Firefox(options=options)
            logger.info("Selenium WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Selenium: {e}")
            self.capture_screenshots = False

    def parse_robots_txt(self, url, session):
        """Parse robots.txt file for a domain"""
        domain = urlparse(url).netloc
        if domain in self.robots_cache:
            return self.robots_cache[domain]

        try:
            robots_url = urljoin(f"http://{domain}", "robots.txt")
            response = session.get(robots_url, timeout=10)
            if response.status_code == 200:
                rules = {
                    'disallow': [],
                    'allow': [],
                    'crawl_delay': None
                }
                for line in response.text.split('\n'):
                    line = line.strip().lower()
                    if line.startswith('disallow:'):
                        rules['disallow'].append(line.split(':', 1)[1].strip())
                    elif line.startswith('allow:'):
                        rules['allow'].append(line.split(':', 1)[1].strip())
                    elif line.startswith('crawl-delay:'):
                        try:
                            rules['crawl_delay'] = float(line.split(':', 1)[1].strip())
                        except ValueError:
                            pass
                self.robots_cache[domain] = rules
                return rules
        except Exception as e:
            logger.debug(f"Error fetching robots.txt for {domain}: {e}")
        
        self.robots_cache[domain] = None
        return None

    def is_allowed_by_robots(self, url, rules):
        """Check if URL is allowed by robots.txt rules"""
        if not rules:
            return True

        path = urlparse(url).path
        
        # Check allow rules first
        for allow in rules['allow']:
            if path.startswith(allow):
                return True
                
        # Then check disallow rules
        for disallow in rules['disallow']:
            if path.startswith(disallow):
                return False
                
        return True

    def capture_screenshot(self, url, output_path):
        """Capture screenshot of a webpage using Selenium"""
        if not self.capture_screenshots:
            return False
            
        try:
            self.driver.get(url)
            time.sleep(5)  # Wait for page to load
            self.driver.save_screenshot(output_path)
            logger.info(f"Screenshot saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error capturing screenshot of {url}: {e}")
            return False

    def export_to_pdf(self, url, content, output_path):
        """Export webpage to PDF using pdfkit"""
        try:
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'quiet': ''
            }
            pdfkit.from_string(content, output_path, options=options)
            logger.info(f"PDF exported to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting {url} to PDF: {e}")
            return False

    def manage_cookies(self, url, response):
        """Manage cookies for the given URL"""
        domain = urlparse(url).netloc
        if 'Set-Cookie' in response.headers:
            self.cookie_jar[domain] = response.cookies
        return self.cookie_jar.get(domain, {})

    def crawl_url(self, tor_session, url, current_depth=0):
        """Enhanced crawl_url method with new features"""
        if current_depth > self.depth or url in self.visited_urls or self.page_count >= self.max_pages:
            return []

        logger.info(f"Crawling: {url} (depth: {current_depth}/{self.depth})")
        self.visited_urls.add(url)
        self.page_count += 1

        try:
            # Check robots.txt if enabled
            if self.respect_robots:
                robots_rules = self.parse_robots_txt(url, tor_session)
                if robots_rules and not self.is_allowed_by_robots(url, robots_rules):
                    logger.info(f"Skipping {url} - disallowed by robots.txt")
                    return []
                if robots_rules and robots_rules['crawl_delay']:
                    time.sleep(robots_rules['crawl_delay'])
            
            # Add random delay
            delay = random.uniform(self.delay_range[0], self.delay_range[1])
            time.sleep(delay)

            # Set up headers with rotating user agent
            headers = {}
            if self.rotate_user_agent:
                headers['User-Agent'] = self.USER_AGENTS[self.current_user_agent_idx]
                self.current_user_agent_idx = (self.current_user_agent_idx + 1) % len(self.USER_AGENTS)

            # Get cookies for this domain
            domain_cookies = self.cookie_jar.get(urlparse(url).netloc, {})
            cookies = {**self.custom_cookies, **domain_cookies}

            # Request the page
            response = tor_session.get(url, headers=headers, cookies=cookies)
            if response.status_code != 200:
                logger.warning(f"Failed to fetch {url}: Status code {response.status_code}")
                return []

            # Update cookie jar
            self.manage_cookies(url, response)

            # Parse content
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract and cache text content
            text_content = self.extract_text_content(soup)
            self.text_content_cache[url] = text_content

            # Analyze content if enabled
            analysis = None
            if self.analyze_content:
                analysis = self.analyze_page(url, html_content, soup)

            # Create domain-specific directory
            domain = urlparse(url).netloc
            domain_dir = os.path.join(self.output_dir, sanitize_filename(domain))
            create_directory(domain_dir)

            # Generate base filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_base = sanitize_filename(f"{urlparse(url).path or 'index'}_{timestamp}")

            # Save HTML content
            html_path = os.path.join(domain_dir, f"{filename_base}.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Save text content
            text_path = os.path.join(domain_dir, f"{filename_base}.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text_content)

            # Save analysis if available
            if analysis:
                analysis_path = os.path.join(domain_dir, f"{filename_base}_analysis.json")
                with open(analysis_path, 'w', encoding='utf-8') as f:
                    json.dump(analysis, f, indent=2)

            # Capture screenshot if enabled
            if self.capture_screenshots:
                screenshot_path = os.path.join(domain_dir, f"{filename_base}.png")
                self.capture_screenshot(url, screenshot_path)

            # Export to PDF if enabled
            if self.export_pdf:
                pdf_path = os.path.join(domain_dir, f"{filename_base}.pdf")
                self.export_to_pdf(url, html_content, pdf_path)

            # Extract and follow links
            links = []
            if current_depth < self.depth:
                links = self.extract_links(soup, url)
                logger.info(f"Found {len(links)} links on {url}")
                
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
        
    def extract_links(self, soup, base_url):
        """Extract and normalize links from page"""
        links = []
        for anchor in soup.find_all('a', href=True):
            href = anchor['href'].strip()
            if href and not href.startswith(('#', 'javascript:', 'mailto:')):
                absolute_url = urljoin(base_url, href)
                if is_valid_onion_url(absolute_url):
                    links.append(absolute_url)
        return links

    def extract_text_content(self, soup):
        """Extract readable text content from page"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
            element.decompose()

        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def analyze_page(self, url, html_content, soup):
        """Analyze page content using AI"""
        if not self.analyze_content:
            return None

        try:
            # Extract text content
            text_content = self.extract_text_content(soup)
            self.text_content_cache[url] = text_content

            if not text_content.strip():
                logger.warning(f"No text content found at {url}")
                return None

            # Get content analysis
            analysis = self.analyzer.analyze_content(text_content)
            entities = self.analyzer.extract_entities(text_content)
            categorization = self.analyzer.categorize_content(text_content)

            # Build complete analysis
            result = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "general_analysis": analysis.get("analysis", ""),
                "entities": entities,
                "categorization": categorization,
                "text_length": len(text_content),
                "language_detection": self.detect_language(text_content),
                "cryptocurrency_addresses": self.extract_crypto_addresses(text_content),
                "contact_info": self.extract_contact_info(text_content)
            }

            return result

        except Exception as e:
            logger.error(f"Error analyzing content from {url}: {e}")
            return None

    def detect_language(self, text):
        """Detect the language of the text"""
        try:
            from langdetect import detect
            return detect(text)
        except:
            return "unknown"

    def extract_crypto_addresses(self, text):
        """Extract cryptocurrency addresses from text"""
        patterns = {
            'bitcoin': r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}',
            'ethereum': r'0x[a-fA-F0-9]{40}',
            'monero': r'4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}'
        }
        
        addresses = {}
        for currency, pattern in patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                addresses[currency] = matches
                
        return addresses

    def extract_contact_info(self, text):
        """Extract contact information from text"""
        patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'telegram': r'@[a-zA-Z0-9_]{5,}',
            'discord': r'[a-zA-Z0-9_]{3,32}#[0-9]{4}'
        }
        
        contact_info = {}
        for contact_type, pattern in patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                contact_info[contact_type] = matches
                
        return contact_info

    def similarity_check(self, url1, url2):
        """Compare similarity between two pages"""
        text1 = self.text_content_cache.get(url1)
        text2 = self.text_content_cache.get(url2)
        
        if not text1 or not text2:
            return None
            
        return SequenceMatcher(None, text1, text2).ratio()

    def start_crawl(self, start_urls):
        """Start the crawling process"""
        start_time = time.time()
        results = {
            "start_time": datetime.now().isoformat(),
            "crawled_pages": 0,
            "visited_urls": [],
            "features_enabled": {
                "screenshots": self.capture_screenshots,
                "pdf_export": self.export_pdf,
                "content_analysis": self.analyze_content,
                "robots_txt": self.respect_robots
            }
        }

        try:
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
        finally:
            if self.capture_screenshots:
                try:
                    self.driver.quit()
                except:
                    pass

        end_time = time.time()
        results["duration_seconds"] = end_time - start_time
        results["end_time"] = datetime.now().isoformat()

        # Save crawl summary
        summary_path = os.path.join(self.output_dir, 
                                  f"crawl_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(summary_path, 'w') as f:
            json.dump(results, f, indent=2)

        logger.info(f"Crawl completed. Visited {self.page_count} pages in {results['duration_seconds']:.2f} seconds")
        return results

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Dark Web Crawler with enhanced features')
    parser.add_argument('--url', '-u', help='Starting URL(s) for crawling (comma-separated)')
    parser.add_argument('--depth', '-d', type=int, default=1, help='Maximum crawl depth')
    parser.add_argument('--output', '-o', default='crawl_results', help='Output directory')
    parser.add_argument('--max-pages', '-m', type=int, default=50, help='Maximum number of pages to crawl')
    parser.add_argument('--no-analysis', action='store_true', help='Disable AI content analysis')
    parser.add_argument('--delay', type=str, default='2-5', help='Delay range between requests (format: min-max)')
    parser.add_argument('--list-file', '-f', help='File containing list of URLs to crawl')
    parser.add_argument('--capture-screenshots', '-s', action='store_true', help='Capture page screenshots')
    parser.add_argument('--export-pdf', '-p', action='store_true', help='Export pages to PDF')
    parser.add_argument('--ignore-robots', action='store_true', help='Ignore robots.txt restrictions')

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
                start_urls.extend([url.strip() for url in f if url.strip() and not url.startswith('#')])
        except Exception as e:
            logger.error(f"Error reading URL list file: {e}")

    # Initialize and start crawler
    crawler = DarkWebCrawler(
        output_dir=args.output,
        depth=args.depth,
        delay_range=delay_range,
        analyze_content=not args.no_analysis,
        max_pages=args.max_pages,
        capture_screenshots=args.capture_screenshots,
        export_pdf=args.export_pdf,
        respect_robots=not args.ignore_robots
    )

    if start_urls:
        crawler.start_crawl(start_urls)
    else:
        logger.error("No URLs provided. Please specify URLs using --url or --list-file")

if __name__ == "__main__":
    main()
