"""
Tor Manager - Handles Tor connection and related utilities
"""
import socket
import time
import logging
from stem import Signal
from stem.control import Controller
from contextlib import contextmanager
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('tor_manager')

class TorManager:
    """
    Manages the Tor connection and provides utilities for accessing the dark web
    """
    def __init__(self, socks_port=9050, control_port=9051, password=None):
        """
        Initialize the Tor manager with specified ports
        """
        self.socks_port = socks_port
        self.control_port = control_port
        self.password = password
        self.session = self._get_tor_session()
        logger.info("Tor Manager initialized")

    def _get_tor_session(self):
        """
        Creates a requests session that routes through Tor
        """
        session = requests.session()
        # Tor uses the SOCKS5 proxy on port 9050 by default
        session.proxies = {
            'http': f'socks5h://127.0.0.1:{self.socks_port}',
            'https': f'socks5h://127.0.0.1:{self.socks_port}'
        }
        return session

    def get_new_identity(self):
        """
        Request a new identity (circuit) from Tor
        """
        try:
            with Controller.from_port(port=self.control_port) as controller:
                if self.password:
                    controller.authenticate(password=self.password)
                else:
                    controller.authenticate()
                controller.signal(Signal.NEWNYM)
                logger.info("New Tor identity obtained")
                # Give the Tor network time to establish new circuits
                time.sleep(5)
                # Refresh the session with the new identity
                self.session = self._get_tor_session()
                return True
        except Exception as e:
            logger.error(f"Failed to get new identity: {e}")
            return False

    def is_tor_running(self):
        """
        Check if Tor is running properly
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', self.socks_port))
            sock.close()
            return result == 0
        except Exception as e:
            logger.error(f"Error checking Tor status: {e}")
            return False

    def get_current_ip(self):
        """
        Get the current exit node IP
        """
        try:
            response = self.session.get('https://check.torproject.org/api/ip')
            data = response.json()
            return data.get('IP', 'Unknown')
        except Exception as e:
            logger.error(f"Error getting current IP: {e}")
            return "Unknown"

    def get(self, url, headers=None, timeout=30, retries=3):
        """
        Send a GET request through Tor
        """
        headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        }
        
        for attempt in range(retries):
            try:
                logger.info(f"Attempting to fetch {url} (attempt {attempt+1}/{retries})")
                response = self.session.get(url, headers=headers, timeout=timeout)
                return response
            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed: {e}")
                if attempt < retries - 1:
                    logger.info("Getting new Tor identity and retrying...")
                    self.get_new_identity()
                    time.sleep(5)  # Wait before retry
                else:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
                    raise

@contextmanager
def tor_session_context():
    """
    Context manager for creating and using a Tor session
    """
    tor = TorManager()
    try:
        if not tor.is_tor_running():
            raise RuntimeError("Tor is not running. Please start the Tor service.")
        logger.info(f"Tor is running. Current IP: {tor.get_current_ip()}")
        yield tor
    finally:
        logger.info("Closing Tor session")
