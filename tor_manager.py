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
        Works with both system Tor and Tor Browser
        """
        # Try both the standard control port and Tor Browser's control port
        control_ports = [self.control_port, 9151]  # 9051 is system Tor, 9151 is Tor Browser
        
        for port in control_ports:
            try:
                logger.info(f"Trying to get new identity using control port {port}")
                with Controller.from_port(port=port) as controller:
                    if self.password:
                        controller.authenticate(password=self.password)
                    else:
                        # Try to authenticate without password
                        try:
                            controller.authenticate()
                        except Exception:
                            # Tor Browser often uses a blank password
                            controller.authenticate("")
                    
                    controller.signal(Signal.NEWNYM)
                    logger.info(f"New Tor identity obtained using control port {port}")
                    
                    # If this worked, update the control port for future use
                    if port != self.control_port:
                        self.control_port = port
                        logger.info(f"Updated control port to {port}")
                    
                    # Give the Tor network time to establish new circuits
                    time.sleep(5)
                    # Refresh the session with the new identity
                    self.session = self._get_tor_session()
                    return True
            except Exception as e:
                logger.debug(f"Failed to get new identity using port {port}: {e}")
                continue
                
        logger.error("Failed to get new identity using any known control port")
        return False

    def is_tor_running(self):
        """
        Check if Tor is running properly - including Tor Browser
        """
        # List of common Tor SOCKS ports to check (system Tor and Tor Browser)
        tor_ports = [self.socks_port, 9150]  # 9050 is system Tor, 9150 is Tor Browser
        
        for port in tor_ports:
            try:
                # Check if the port is open
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                
                if result == 0:
                    # Port is open, now verify it's actually Tor by making a test connection
                    test_session = requests.session()
                    test_session.proxies = {
                        'http': f'socks5h://127.0.0.1:{port}',
                        'https': f'socks5h://127.0.0.1:{port}'
                    }
                    
                    try:
                        # Try to connect to a Tor-specific service
                        response = test_session.get('https://check.torproject.org/', timeout=5)
                        if 'Congratulations' in response.text:
                            # If this port works, update the object's port to match
                            if port != self.socks_port:
                                logger.info(f"Found Tor running on port {port} (likely Tor Browser)")
                                self.socks_port = port
                                # Refresh the session with the new port
                                self.session = self._get_tor_session()
                            return True
                    except Exception as e:
                        logger.debug(f"Port {port} is open but doesn't appear to be Tor: {e}")
                        continue
            except Exception as e:
                logger.debug(f"Error checking Tor on port {port}: {e}")
        
        logger.error("No running Tor service found. Please start Tor or Tor Browser.")
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
            raise RuntimeError("Tor is not running. Please start Tor Browser or the Tor service.")
        logger.info(f"Tor is running. Current IP: {tor.get_current_ip()}")
        yield tor
    finally:
        logger.info("Closing Tor session")
