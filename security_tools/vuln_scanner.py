"""
Enhanced Vulnerability Scanner with additional security checks
"""
import re
import socket
import requests
import json
import logging
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def _check_cors(self, result: Dict[str, Any], header: str, value: str) -> None:
        """Check CORS configuration for security issues"""
        if value == '*':
            result['vulnerabilities'].append({
                'type': 'cors_misconfiguration',
                'header': header,
                'value': value,
                'severity': 'high',
                'description': 'CORS is configured to allow all origins (*)'
            })
        elif value:
            try:
                from urllib.parse import urlparse
                parsed = urlparse(value)
                if not parsed.scheme or not parsed.netloc:
                    result['vulnerabilities'].append({
                        'type': 'cors_misconfiguration',
                        'header': header,
                        'value': value,
                        'severity': 'medium',
                        'description': 'CORS origin is not properly formatted'
                    })
            except Exception:
                result['vulnerabilities'].append({
                    'type': 'cors_misconfiguration',
                    'header': header,
                    'value': value,
                    'severity': 'medium',
                    'description': 'Invalid CORS origin format'
                })


logger = logging.getLogger(__name__)

class VulnerabilityScanner:
    """
    Scanner for detecting common vulnerabilities in websites and servers
    """
    def __init__(self, ai_analyzer=None):
        """
        Initialize the vulnerability scanner

        Args:
            ai_analyzer: Optional AI analyzer component for enhanced analysis
        """
        self.ai_analyzer = ai_analyzer
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
        }

    def is_valid_ip(self, ip: str) -> bool:
        """
        Check if a string is a valid IP address

        Args:
            ip: String to check

        Returns:
            Boolean indicating if string is a valid IP
        """
        pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
        match = re.match(pattern, ip)
        if not match:
            return False

        for i in range(1, 5):
            octet = int(match.group(i))
            if octet < 0 or octet > 255:
                return False

        return True

    def is_valid_domain(self, domain: str) -> bool:
        """
        Check if a string is a valid domain name

        Args:
            domain: String to check

        Returns:
            Boolean indicating if string is a valid domain
        """
        # Basic domain validation
        pattern = r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
        return bool(re.match(pattern, domain))

    def normalize_target(self, target: str) -> str:
        """
        Normalize the target string to a standard format

        Args:
            target: Target string (IP or domain)

        Returns:
            Normalized target URL
        """
        target = target.strip().lower()

        # If it doesn't start with http/https, add it
        if not target.startswith(("http://", "https://")):
            target = "http://" + target

        return target

    def get_ip_from_domain(self, domain: str) -> Optional[str]:
        """
        Resolve domain name to IP address

        Args:
            domain: Domain name to resolve

        Returns:
            IP address string or None if resolution fails
        """
        try:
            parsed = urlparse(domain)
            hostname = parsed.netloc or parsed.path
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            logger.error(f"Could not resolve domain: {domain}")
            return None

    def scan_target(self, target: str) -> Dict[str, Any]:
        """
        Scan a target for vulnerabilities

        Args:
            target: Target URL, domain or IP address

        Returns:
            Dictionary with scan results
        """
        result = {
            "target": target,
            "normalized_target": self.normalize_target(target),
            "status": "error",
            "vulnerabilities": [],
            "info": {},
            "headers": {},
            "timestamp": None
        }

        normalized = result["normalized_target"]

        try:
            logger.info(f"Starting scan of {normalized}")

            # Make a request to the target
            response = requests.get(normalized, headers=self.headers, timeout=10, verify=False)
            result["status"] = "completed"
            result["info"]["status_code"] = response.status_code
            result["headers"] = dict(response.headers)

            # Basic header analysis
            self._analyze_headers(result, response.headers)

            # Content analysis
            if "text/html" in response.headers.get("Content-Type", ""):
                self._analyze_html_content(result, response.text)

            # Port scan if it's an IP or we can resolve to IP
            domain = urlparse(normalized).netloc
            if self.is_valid_ip(domain):
                ip = domain
            else:
                ip = self.get_ip_from_domain(normalized)

            if ip:
                result["info"]["ip"] = ip
                self._scan_common_ports(result, ip)

            # Enhance with AI analysis if available
            if self.ai_analyzer and response.text:
                try:
                    ai_results = self._run_ai_analysis(normalized, response.text, result)
                    if ai_results:
                        result["ai_analysis"] = ai_results
                except Exception as e:
                    logger.error(f"AI analysis failed: {str(e)}")
                    result["ai_analysis_error"] = str(e)

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Error scanning {normalized}: {str(e)}")
            result["status"] = "error"
            result["error"] = str(e)
            return result

    def _analyze_headers(self, result: Dict[str, Any], headers: Any) -> None:
        """Enhanced header analysis with modern security checks"""
        security_headers = {
            'X-XSS-Protection': {'required': True, 'recommended': '1; mode=block'},
            'X-Content-Type-Options': {'required': True, 'recommended': 'nosniff'},
            'X-Frame-Options': {'required': True, 'recommended': ['DENY', 'SAMEORIGIN']},
            'Content-Security-Policy': {'required': True},
            'Strict-Transport-Security': {'required': True},
            'Referrer-Policy': {'required': False, 'recommended': 'strict-origin-when-cross-origin'},
            'Permissions-Policy': {'required': True},
            'Cross-Origin-Embedder-Policy': {'required': False},
            'Cross-Origin-Opener-Policy': {'required': False},
            'Cross-Origin-Resource-Policy': {'required': False},
            'Access-Control-Allow-Origin': {'required': False, 'check': self._check_cors},
            'Expect-CT': {'required': False},
            'Report-To': {'required': False},
            'NEL': {'required': False}
        }
            'X-XSS-Protection': {'required': True, 'recommended': '1; mode=block'},
            'X-Content-Type-Options': {'required': True, 'recommended': 'nosniff'},
            'X-Frame-Options': {'required': True, 'recommended': ['DENY', 'SAMEORIGIN']},
            'Content-Security-Policy': {'required': True},
            'Strict-Transport-Security': {'required': True},
            'Referrer-Policy': {'required': False, 'recommended': 'strict-origin-when-cross-origin'},
            'Feature-Policy': {'required': False},
            'Access-Control-Allow-Origin': {'required': False, 'check': self._check_cors}
        }

        for header, requirements in security_headers.items():
            if header not in headers:
                if requirements.get('required', False):
                    severity = 'critical' if header in ['Content-Security-Policy', 'Strict-Transport-Security'] else 'high'
                    result['vulnerabilities'].append({
                        'type': 'missing_security_header',
                        'header': header,
                        'severity': 'high',
                        'description': f'Missing required security header: {header}'
                    })
            else:
                value = headers[header]
                if 'recommended' in requirements:
                    recommended = requirements['recommended']
                    if isinstance(recommended, list):
                        if value not in recommended:
                            result['vulnerabilities'].append({
                                'type': 'weak_security_header',
                                'header': header,
                                'value': value,
                                'recommended': recommended,
                                'severity': 'medium',
                                'description': f'Security header {header} has weak value: {value}'
                            })
                    elif value != recommended:
                        result['vulnerabilities'].append({
                            'type': 'weak_security_header',
                            'header': header,
                            'value': value,
                            'recommended': recommended,
                            'severity': 'medium',
                            'description': f'Security header {header} has weak value: {value}'
                        })

                if 'check' in requirements:
                    requirements['check'](result, header, value)

        # Check for information disclosure
        sensitive_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version', 'X-AspNetMvc-Version']
        for header in sensitive_headers:
            if header in headers:
                result['vulnerabilities'].append({
                    'type': 'information_disclosure',
                    'header': header,
                    'value': headers[header],
                    'severity': 'low',
                    'description': f'Header {header} reveals technology information'
                })


    def analyze_ssl_cert(self, hostname: str) -> Dict[str, Any]:
        """Analyze SSL/TLS certificate"""
        try:
            import ssl
            import socket

            context = ssl.create_default_context()
            with context.wrap_socket(socket.socket(), server_hostname=hostname) as sock:
                sock.connect((hostname, 443))
                cert = sock.getpeercert()

                return {
                    "subject": dict(x[0] for x in cert['subject']),
                    "issuer": dict(x[0] for x in cert['issuer']),
                    "version": cert['version'],
                    "serialNumber": cert['serialNumber'],
                    "notBefore": cert['notBefore'],
                    "notAfter": cert['notAfter']
                }
        except Exception as e:
            return {"error": str(e)}

    def _analyze_html_content(self, result: Dict[str, Any], content: str) -> None:
        """
        Analyze HTML content for vulnerabilities

        Args:
            result: Scan result dictionary to update
            content: HTML content string
        """
        soup = BeautifulSoup(content, "html.parser")

        # Check for forms without CSRF protection
        forms = soup.find_all("form")
        for form in forms:
            if not form.find("input", attrs={"type": "hidden", "name": re.compile(r"csrf|token", re.I)}):
                result["vulnerabilities"].append({
                    "type": "csrf_vulnerability",
                    "name": "Form without CSRF protection",
                    "severity": "high",
                    "description": "A form was found without a CSRF token, making it vulnerable to Cross-Site Request Forgery attacks."
                })

        # Check for insecure cookies (no HttpOnly, no Secure flag)
        if "Set-Cookie" in result["headers"]:
            cookies = result["headers"]["Set-Cookie"].split(",")
            for cookie in cookies:
                if "httponly" not in cookie.lower():
                    result["vulnerabilities"].append({
                        "type": "insecure_cookie",
                        "name": "Cookie without HttpOnly flag",
                        "severity": "medium",
                        "description": "Cookies without the HttpOnly flag can be accessed by malicious JavaScript, enabling session hijacking."
                    })
                if "secure" not in cookie.lower() and result["normalized_target"].startswith("https"):
                    result["vulnerabilities"].append({
                        "type": "insecure_cookie",
                        "name": "Cookie without Secure flag",
                        "severity": "medium",
                        "description": "Cookies without the Secure flag can be transmitted over unencrypted connections, enabling eavesdropping."
                    })

        # Check for potentially vulnerable JavaScript libraries
        scripts = soup.find_all("script", src=True)
        for script in scripts:
            src = script["src"]
            # Check for known vulnerable libraries (would need a database of vulnerable versions)
            if "jquery" in src.lower() and re.search(r"jquery[.-]([0-2]\.[0-9]+\.[0-9]+)", src.lower()):
                result["vulnerabilities"].append({
                    "type": "outdated_library",
                    "name": "Potentially outdated jQuery library",
                    "severity": "medium",
                    "description": f"Found a potentially outdated jQuery library: {src}. Outdated libraries may contain known security vulnerabilities."
                })

    def analyze_network_traffic(self, target: str, duration: int = 30) -> Dict[str, Any]:
        """Analyze network traffic patterns for the target"""
        try:
            from scapy.all import sniff, IP
            packets = sniff(filter=f"host {target}", timeout=duration)
            
            analysis = {
                "total_packets": len(packets),
                "protocols": {},
                "source_ips": set(),
                "dest_ips": set(),
                "suspicious_patterns": []
            }
            
            for pkt in packets:
                if IP in pkt:
                    # Analyze protocols
                    proto = pkt[IP].proto
                    analysis["protocols"][proto] = analysis["protocols"].get(proto, 0) + 1
                    
                    # Track IPs
                    analysis["source_ips"].add(pkt[IP].src)
                    analysis["dest_ips"].add(pkt[IP].dst)
                    
                    # Check for suspicious patterns
                    if proto == 6:  # TCP
                        if pkt.dport in [22, 23, 3389]:  # Common attack ports
                            analysis["suspicious_patterns"].append({
                                "type": "potential_brute_force",
                                "port": pkt.dport,
                                "source": pkt[IP].src
                            })
            
            return analysis
        except Exception as e:
            return {"error": str(e)}

    def _scan_common_ports(self, result: Dict[str, Any], ip: str) -> None:
        """
        Scan common ports on the target IP

        Args:
            result: Scan result dictionary to update
            ip: IP address to scan
        """
        common_ports = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            135: "RPC",
            139: "NetBIOS",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            1433: "MSSQL",
            1521: "Oracle",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            8080: "HTTP-Proxy"
        }

        open_ports = []

        # Only scan a few ports for the demo to avoid timeouts
        for port in [80, 443, 22, 21, 3389]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result_code = sock.connect_ex((ip, port))
                if result_code == 0:
                    service = common_ports.get(port, "Unknown")
                    open_ports.append({"port": port, "service": service})

                    # Add specific vulnerabilities based on open ports
                    if port == 21:
                        result["vulnerabilities"].append({
                            "type": "open_port",
                            "name": "FTP Service Exposed",
                            "severity": "medium",
                            "description": "FTP service is running and exposed to the internet. Consider using SFTP instead or restricting access."
                        })
                    elif port == 23:
                        result["vulnerabilities"].append({
                            "type": "open_port",
                            "name": "Telnet Service Exposed",
                            "severity": "high",
                            "description": "Telnet service is running and exposed to the internet. Telnet transmits data in cleartext and should be replaced with SSH."
                        })
                sock.close()
            except socket.error:
                pass

        result["info"]["open_ports"] = open_ports

    def _run_ai_analysis(self, url: str, content: str, scan_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Run AI analysis on the target

        Args:
            url: Target URL
            content: HTML content
            scan_result: Current scan result to enhance

        Returns:
            Dictionary with AI analysis results or None if AI not available
        """
        if not self.ai_analyzer:
            return None

        try:
            # Use only the first 5000 characters to avoid overloading the AI model
            content_sample = content[:5000]

            # Create a prompt for vulnerability analysis
            prompt = f"""
            Analyze this website content for potential security vulnerabilities.
            URL: {url}

            Content sample:
            {content_sample}

            Scan data:
            {json.dumps(scan_result, indent=2)}

            Please identify any security vulnerabilities, including but not limited to:
            1. Cross-Site Scripting (XSS) vulnerabilities
            2. SQL Injection possibilities
            3. Security misconfigurations
            4. Sensitive data exposure
            5. Known vulnerabilities in detected frameworks

            Format your response as a JSON object with these fields:
            {{
                "identified_vulnerabilities": [
                    {{
                        "type": "vulnerability type",
                        "severity": "low/medium/high/critical",
                        "description": "detailed description",
                        "mitigation": "how to fix this issue"
                    }}
                ],
                "risk_assessment": "overall risk assessment",
                "recommended_actions": ["action1", "action2"]
            }}
            """

            # Call the AI analyzer with the prompt
            analysis_result = self.ai_analyzer.analyze_content(prompt)

            # Extract the actual result from the AI response
            if isinstance(analysis_result, dict) and "response" in analysis_result:
                # Try to parse the response as JSON
                try:
                    vulnerabilities = json.loads(analysis_result["response"])
                    return vulnerabilities
                except json.JSONDecodeError:
                    # If it's not valid JSON, return the raw text
                    return {"raw_analysis": analysis_result["response"]}

            return analysis_result

        except Exception as e:
            logger.error(f"Error during AI analysis: {str(e)}")
            return {"error": str(e)}