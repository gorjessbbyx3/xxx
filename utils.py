"""
Utility functions for the dark web crawler
"""

import os
import re
import string
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('utils')

def sanitize_filename(filename):
    """
    Sanitize a string to be used as a filename
    
    Args:
        filename: The string to sanitize
        
    Returns:
        Sanitized string valid for use as a filename
    """
    # Replace path separators with underscores
    sanitized = filename.replace('/', '_').replace('\\', '_')
    
    # Remove URL parameters, fragments, and other special characters
    sanitized = re.sub(r'[\?&=;#]', '_', sanitized)
    
    # Replace any remaining invalid characters
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c if c in valid_chars else '_' for c in sanitized)
    
    # Limit filename length
    if len(sanitized) > 255:
        sanitized = sanitized[:255]
    
    # Handle empty filenames
    if not sanitized or sanitized.isspace():
        sanitized = "unnamed_file"
    
    return sanitized

def create_directory(directory_path):
    """
    Create a directory if it doesn't exist
    
    Args:
        directory_path: Path of directory to create
        
    Returns:
        Boolean indicating success
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logger.info(f"Created directory: {directory_path}")
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory_path}: {e}")
        return False

def is_valid_onion_url(url):
    """
    Check if a URL is a valid .onion URL
    
    Args:
        url: URL to check
        
    Returns:
        Boolean indicating if URL is a valid .onion URL
    """
    try:
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Check onion domain
        if not parsed.netloc.endswith('.onion'):
            return False
        
        # v3 onion addresses are 56 characters + .onion (62 total)
        # v2 onion addresses are 16 characters + .onion (22 total)
        hostname = parsed.netloc
        if hostname.count('.') == 1:
            onion_name = hostname.split('.')[0]
            return (len(onion_name) == 16 or len(onion_name) == 56) and all(c in string.ascii_lowercase + string.digits for c in onion_name)
        
        return False
    except Exception:
        return False

def get_domain_from_url(url):
    """
    Extract domain from URL
    
    Args:
        url: URL to extract domain from
        
    Returns:
        Domain string
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return url
