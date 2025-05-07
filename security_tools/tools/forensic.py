"""
Digital Forensics Tools
"""

from security_tools.core import HackingTool, HackingToolsCollection


class AutopsyTool(HackingTool):
    TITLE = "Autopsy"
    DESCRIPTION = "Digital forensics platform for analyzing disk images and recovering files"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install autopsy"]
    RUN_COMMANDS = ["autopsy"]
    PROJECT_URL = "https://www.autopsy.com/"


class WiresharkTool(HackingTool):
    TITLE = "Wireshark"
    DESCRIPTION = "Network protocol analyzer for examining network traffic"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install wireshark"]
    RUN_COMMANDS = ["wireshark"]
    PROJECT_URL = "https://www.wireshark.org/"


class BulkExtractorTool(HackingTool):
    TITLE = "Bulk Extractor"
    DESCRIPTION = "Extracts useful information without parsing filesystem structure"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install bulk-extractor"]
    RUN_COMMANDS = ["bulk_extractor -h"]
    PROJECT_URL = "https://github.com/simsong/bulk_extractor"


class DiskImageAcquireTool(HackingTool):
    TITLE = "Disk Clone and ISO Image Acquire"
    DESCRIPTION = "Create forensically sound disk images for analysis"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install guymager"]
    RUN_COMMANDS = ["guymager"]
    PROJECT_URL = "https://guymager.sourceforge.io/"


class VolatilityTool(HackingTool):
    TITLE = "Volatility3"
    DESCRIPTION = "Advanced memory forensics framework for analyzing RAM dumps"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = [
        "git clone https://github.com/volatilityfoundation/volatility3.git",
        "cd volatility3 && pip install -r requirements.txt"
    ]
    RUN_COMMANDS = ["cd volatility3 && python vol.py -h"]
    PROJECT_URL = "https://github.com/volatilityfoundation/volatility3/"


class ForemanTool(HackingTool):
    TITLE = "Foremost"
    DESCRIPTION = "File recovery tool based on file headers and footers"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install foremost"]
    RUN_COMMANDS = ["foremost -h"]
    PROJECT_URL = "http://foremost.sourceforge.net/"


class BinwalkTool(HackingTool):
    TITLE = "Binwalk"
    DESCRIPTION = "Firmware analysis tool for searching embedded files and executable code"
    CATEGORY = "Forensic Tools"
    INSTALL_COMMANDS = ["sudo apt-get install binwalk"]
    RUN_COMMANDS = ["binwalk -h"]
    PROJECT_URL = "https://github.com/ReFirmLabs/binwalk"


class ForensicTools(HackingToolsCollection):
    TITLE = "Forensic Tools"
    DESCRIPTION = "Tools for digital forensics and incident response"
    
    TOOLS = [
        AutopsyTool(),
        WiresharkTool(),
        BulkExtractorTool(),
        DiskImageAcquireTool(),
        VolatilityTool(),
        ForemanTool(),
        BinwalkTool()
    ]
"""
Forensic analysis tools including steganography detection
"""
import os
import cv2
import numpy as np
from PIL import Image

class SteganographyDetector:
    """Enhanced steganography and forensics detector"""
    
    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']
        self.metadata_analyzers = {
            'image': ['exif', 'icc_profile', 'xmp'],
            'document': ['pdf_metadata', 'office_metadata'],
            'audio': ['id3', 'vorbis_comment'],
            'video': ['mkv_metadata', 'mp4_metadata']
        }
        self.analysis_modes = ['basic', 'deep', 'ml_enhanced']

    def analyze_image(self, image_path: str) -> dict:
        """Analyze image for potential hidden data"""
        if not os.path.exists(image_path):
            return {"error": "Image file not found"}

        ext = os.path.splitext(image_path)[1].lower()
        if ext not in self.supported_formats:
            return {"error": "Unsupported image format"}

        results = {
            "file_info": self._get_file_info(image_path),
            "statistical_analysis": self._analyze_statistics(image_path),
            "suspicious_patterns": self._detect_patterns(image_path)
        }

        return results

    def _get_file_info(self, image_path: str) -> dict:
        """Get basic file information"""
        stats = os.stat(image_path)
        return {
            "size": stats.st_size,
            "created": stats.st_ctime,
            "modified": stats.st_mtime
        }

    def _analyze_statistics(self, image_path: str) -> dict:
        """Analyze image statistics for anomalies"""
        img = cv2.imread(image_path)
        if img is None:
            return {"error": "Failed to read image"}

        hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
        hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])

        return {
            "mean_values": {
                "blue": np.mean(hist_b),
                "green": np.mean(hist_g),
                "red": np.mean(hist_r)
            },
            "std_dev": {
                "blue": np.std(hist_b),
                "green": np.std(hist_g),
                "red": np.std(hist_r)
            }
        }

    def _detect_patterns(self, image_path: str) -> list:
        """Detect suspicious patterns indicating steganography"""
        suspicious = []
        img = Image.open(image_path)
        
        # Check for unusual bit patterns
        pixels = list(img.getdata())
        lsb_ones = 0
        total_pixels = len(pixels)

        for pixel in pixels:
            if isinstance(pixel, int):
                if pixel & 1:
                    lsb_ones += 1
            else:
                for value in pixel:
                    if value & 1:
                        lsb_ones += 1

        lsb_ratio = lsb_ones / (total_pixels * len(pixels[0]) if isinstance(pixels[0], tuple) else total_pixels)
        
        if abs(lsb_ratio - 0.5) < 0.01:
            suspicious.append({
                "type": "uniform_lsb_distribution",
                "description": "Unusually uniform LSB distribution suggests hidden data"
            })

        return suspicious
