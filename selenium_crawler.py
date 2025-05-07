
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('selenium_crawler')

class SeleniumCrawler:
    def __init__(self, headless=True):
        """Initialize Selenium crawler with Firefox in headless mode by default"""
        self.options = webdriver.FirefoxOptions()
        if headless:
            self.options.add_argument('--headless')
        
        # Additional privacy options
        self.options.set_preference("privacy.trackingprotection.enabled", True)
        self.options.set_preference("network.cookie.cookieBehavior", 2)
        
        self.driver = None
        self.wait = None
    
    def start(self):
        """Start the browser session"""
        try:
            self.driver = webdriver.Firefox(options=self.options)
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("Browser session started successfully")
            return True
        except WebDriverException as e:
            logger.error(f"Failed to start browser: {e}")
            return False
    
    def stop(self):
        """Stop the browser session"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser session stopped")
    
    def navigate(self, url):
        """Navigate to a URL"""
        try:
            self.driver.get(url)
            return True
        except WebDriverException as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            return False
    
    def get_page_source(self):
        """Get the current page source"""
        return self.driver.page_source
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timeout waiting for element: {value}")
            return None
    
    def screenshot(self, filename):
        """Take a screenshot of the current page"""
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved to {filename}")
            return True
        except WebDriverException as e:
            logger.error(f"Failed to take screenshot: {e}")
            return False
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Allow time for content to load

def main():
    """Example usage"""
    crawler = SeleniumCrawler(headless=True)
    
    if crawler.start():
        # Example navigation
        crawler.navigate("https://example.com")
        
        # Wait for specific element
        element = crawler.wait_for_element(By.TAG_NAME, "h1")
        if element:
            print(f"Found heading: {element.text}")
        
        # Take screenshot
        crawler.screenshot("example.png")
        
        # Clean up
        crawler.stop()

if __name__ == "__main__":
    main()
