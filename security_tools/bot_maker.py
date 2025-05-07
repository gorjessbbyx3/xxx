"""
Bot Maker - Tool for creating and controlling various types of bots for security testing
"""
import random
import string
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
import threading
import socket
import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BotMaker:
    """
    Creates and manages various types of interactive bots for security testing and automation
    """
    def __init__(self, tor_manager=None, ai_analyzer=None):
        """
        Initialize the bot maker
        
        Args:
            tor_manager: Optional TorManager instance for anonymous bot connections
            ai_analyzer: Optional AI analyzer for content understanding
        """
        self.tor_manager = tor_manager
        self.ai_analyzer = ai_analyzer
        self.active_bots = {}
        self.task_queue = {}  # Stores tasks queued for each bot
        self.interaction_results = {}  # Stores results of user interactions
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        ]
        
    def generate_bot_id(self) -> str:
        """
        Generate a unique ID for a bot
        
        Returns:
            Unique bot ID string
        """
        timestamp = int(time.time())
        random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"bot_{timestamp}_{random_part}"
        
    def create_web_crawler_bot(self, start_urls: List[str], max_depth: int = 3, max_pages: int = 100, 
                              delay_range: Tuple[float, float] = (2.0, 5.0), 
                              keywords: Optional[List[str]] = None,
                              use_tor: bool = False, 
                              user_agent: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a web crawler bot that systematically browses websites
        
        Args:
            start_urls: List of URLs to start crawling from
            max_depth: Maximum crawl depth
            max_pages: Maximum number of pages to crawl
            delay_range: Random delay range between requests (min, max) in seconds
            keywords: Optional keywords to search for in content
            use_tor: Whether to route through Tor
            user_agent: Optional user agent string to use
            
        Returns:
            Dictionary with bot details
        """
        bot_id = self.generate_bot_id()
        
        if not user_agent:
            user_agent = random.choice(self.user_agents)
            
        bot_config = {
            "id": bot_id,
            "type": "web_crawler",
            "start_urls": start_urls,
            "max_depth": max_depth,
            "max_pages": max_pages,
            "delay_range": delay_range,
            "keywords": keywords or [],
            "use_tor": use_tor,
            "user_agent": user_agent,
            "status": "created",
            "visited_urls": [],
            "found_content": [],
            "created_at": datetime.now().isoformat(),
            "thread": None
        }
        
        self.active_bots[bot_id] = bot_config
        
        return {
            "bot_id": bot_id,
            "type": "web_crawler",
            "status": "created",
            "config": bot_config
        }
        
    def create_chat_bot(self, platform: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a chat bot for automated interactions
        
        Args:
            platform: Chat platform name (e.g., "discord", "telegram", "irc")
            config: Platform-specific configuration
            
        Returns:
            Dictionary with bot details
        """
        bot_id = self.generate_bot_id()
        
        supported_platforms = ["discord", "telegram", "irc", "slack", "custom"]
        if platform not in supported_platforms:
            return {
                "error": f"Unsupported platform. Supported platforms: {', '.join(supported_platforms)}"
            }
            
        bot_config = {
            "id": bot_id,
            "type": "chat_bot",
            "platform": platform,
            "platform_config": config,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "thread": None,
            "log": []
        }
        
        # Validate platform-specific configuration
        if platform == "discord":
            required_fields = ["token", "channels"]
            if not all(field in config for field in required_fields):
                return {
                    "error": f"Missing required configuration fields for Discord bot: {', '.join(required_fields)}"
                }
        elif platform == "telegram":
            required_fields = ["api_id", "api_hash", "phone", "channel_ids"]
            if not all(field in config for field in required_fields):
                return {
                    "error": f"Missing required configuration fields for Telegram bot: {', '.join(required_fields)}"
                }
        # Add validation for other platforms as needed
        
        self.active_bots[bot_id] = bot_config
        
        return {
            "bot_id": bot_id,
            "type": "chat_bot",
            "platform": platform,
            "status": "created"
        }
        
    def create_social_media_bot(self, platform: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a social media bot for automated posting and interactions
        
        Args:
            platform: Social media platform name (e.g., "twitter", "reddit", "facebook")
            config: Platform-specific configuration
            
        Returns:
            Dictionary with bot details
        """
        bot_id = self.generate_bot_id()
        
        supported_platforms = ["twitter", "reddit", "facebook", "instagram", "custom"]
        if platform not in supported_platforms:
            return {
                "error": f"Unsupported platform. Supported platforms: {', '.join(supported_platforms)}"
            }
            
        bot_config = {
            "id": bot_id,
            "type": "social_media_bot",
            "platform": platform,
            "platform_config": config,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "thread": None,
            "activity_log": []
        }
        
        # Validate platform-specific configuration
        if platform == "twitter":
            required_fields = ["api_key", "api_secret", "access_token", "access_token_secret"]
            if not all(field in config for field in required_fields):
                return {
                    "error": f"Missing required configuration fields for Twitter bot: {', '.join(required_fields)}"
                }
        elif platform == "reddit":
            required_fields = ["client_id", "client_secret", "username", "password", "user_agent"]
            if not all(field in config for field in required_fields):
                return {
                    "error": f"Missing required configuration fields for Reddit bot: {', '.join(required_fields)}"
                }
        # Add validation for other platforms as needed
        
        self.active_bots[bot_id] = bot_config
        
        return {
            "bot_id": bot_id,
            "type": "social_media_bot",
            "platform": platform,
            "status": "created"
        }
        
    def create_ddos_simulator_bot(self, target: str, method: str, duration: int,
                                 rate: int, use_tor: bool = False) -> Dict[str, Any]:
        """
        Create a DDoS simulation bot for controlled testing on approved targets
        
        Args:
            target: Target URL or IP address
            method: Attack method (e.g., "http_flood", "syn_flood", "slowloris")
            duration: Duration in seconds
            rate: Request rate per second
            use_tor: Whether to route through Tor
            
        Returns:
            Dictionary with bot details
        """
        # IMPORTANT: This is for educational and authorized testing purposes only
        # Real DDoS attacks are illegal and unethical
        
        bot_id = self.generate_bot_id()
        
        supported_methods = ["http_flood", "syn_flood", "slowloris", "udp_flood"]
        if method not in supported_methods:
            return {
                "error": f"Unsupported method. Supported methods: {', '.join(supported_methods)}"
            }
            
        # Impose safety limits
        if duration > 30:
            duration = 30  # Cap at 30 seconds for safety
        if rate > 10:
            rate = 10  # Cap at 10 requests per second for safety
            
        bot_config = {
            "id": bot_id,
            "type": "ddos_simulator",
            "target": target,
            "method": method,
            "duration": duration,
            "rate": rate,
            "use_tor": use_tor,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "thread": None,
            "disclaimer": "This simulator is for educational purposes only. "
                         "Real DDoS attacks are illegal and unethical."
        }
        
        self.active_bots[bot_id] = bot_config
        
        return {
            "bot_id": bot_id,
            "type": "ddos_simulator",
            "status": "created",
            "warning": "Use only on systems you own or have explicit permission to test."
        }
        
    def create_network_scanner_bot(self, target: str, scan_type: str, 
                                  port_range: Optional[List[int]] = None,
                                  use_tor: bool = False) -> Dict[str, Any]:
        """
        Create a network scanner bot for security testing
        
        Args:
            target: Target IP, domain, or CIDR range
            scan_type: Type of scan (e.g., "port_scan", "service_detection", "os_detection")
            port_range: Optional port range to scan
            use_tor: Whether to route through Tor
            
        Returns:
            Dictionary with bot details
        """
        bot_id = self.generate_bot_id()
        
        supported_scan_types = ["port_scan", "service_detection", "os_detection", "vulnerability_scan"]
        if scan_type not in supported_scan_types:
            return {
                "error": f"Unsupported scan type. Supported types: {', '.join(supported_scan_types)}"
            }
            
        # Default port range if not specified
        if not port_range:
            port_range = [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 3389, 8080]
            
        bot_config = {
            "id": bot_id,
            "type": "network_scanner",
            "target": target,
            "scan_type": scan_type,
            "port_range": port_range,
            "use_tor": use_tor,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "thread": None,
            "results": {},
            "disclaimer": "This scanner is for educational and authorized testing purposes only. "
                         "Unauthorized scanning may be illegal in some jurisdictions."
        }
        
        self.active_bots[bot_id] = bot_config
        
        return {
            "bot_id": bot_id,
            "type": "network_scanner",
            "status": "created",
            "warning": "Use only on systems you own or have explicit permission to test."
        }

    def create_crypto_miner_bot(self, network: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a simulated cryptocurrency mining bot (for educational purposes only)
        
        Args:
            network: Cryptocurrency network (e.g., "bitcoin", "ethereum", "monero")
            config: Network-specific configuration
            
        Returns:
            Dictionary with bot details
        """
        bot_id = self.generate_bot_id()
        
        supported_networks = ["bitcoin", "ethereum", "monero", "litecoin"]
        if network not in supported_networks:
            return {
                "error": f"Unsupported network. Supported networks: {', '.join(supported_networks)}"
            }
            
        bot_config = {
            "id": bot_id,
            "type": "crypto_miner_sim",
            "network": network,
            "network_config": config,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "thread": None,
            "mining_statistics": {
                "start_time": None,
                "end_time": None,
                "blocks_found": 0,
                "hash_rate": "0 H/s",
                "estimated_earnings": 0
            },
            "disclaimer": "This is a simulated miner for educational purposes only."
        }
        
        self.active_bots[bot_id] = bot_config
        
        return {
            "bot_id": bot_id,
            "type": "crypto_miner_sim",
            "network": network,
            "status": "created"
        }
        
    def start_bot(self, bot_id: str) -> Dict[str, Any]:
        """
        Start a previously created bot
        
        Args:
            bot_id: ID of the bot to start
            
        Returns:
            Dictionary with start result
        """
        if bot_id not in self.active_bots:
            return {"error": f"Bot with ID {bot_id} not found"}
            
        bot = self.active_bots[bot_id]
        
        if bot["status"] == "running":
            return {"error": f"Bot with ID {bot_id} is already running"}
            
        # Start the appropriate bot type
        if bot["type"] == "web_crawler":
            thread = threading.Thread(target=self._run_web_crawler_bot, args=(bot_id,))
            thread.daemon = True
            thread.start()
            bot["thread"] = thread
            bot["status"] = "running"
            bot["start_time"] = datetime.now().isoformat()
            
        elif bot["type"] == "chat_bot":
            thread = threading.Thread(target=self._run_chat_bot, args=(bot_id,))
            thread.daemon = True
            thread.start()
            bot["thread"] = thread
            bot["status"] = "running"
            bot["start_time"] = datetime.now().isoformat()
            
        elif bot["type"] == "social_media_bot":
            thread = threading.Thread(target=self._run_social_media_bot, args=(bot_id,))
            thread.daemon = True
            thread.start()
            bot["thread"] = thread
            bot["status"] = "running"
            bot["start_time"] = datetime.now().isoformat()
            
        elif bot["type"] == "ddos_simulator":
            thread = threading.Thread(target=self._run_ddos_simulator, args=(bot_id,))
            thread.daemon = True
            thread.start()
            bot["thread"] = thread
            bot["status"] = "running"
            bot["start_time"] = datetime.now().isoformat()
            
        elif bot["type"] == "network_scanner":
            thread = threading.Thread(target=self._run_network_scanner, args=(bot_id,))
            thread.daemon = True
            thread.start()
            bot["thread"] = thread
            bot["status"] = "running"
            bot["start_time"] = datetime.now().isoformat()
            
        elif bot["type"] == "crypto_miner_sim":
            thread = threading.Thread(target=self._run_crypto_miner_sim, args=(bot_id,))
            thread.daemon = True
            thread.start()
            bot["thread"] = thread
            bot["status"] = "running"
            bot["start_time"] = datetime.now().isoformat()
            
        else:
            return {"error": f"Unknown bot type: {bot['type']}"}
            
        return {
            "bot_id": bot_id,
            "type": bot["type"],
            "status": "running",
            "start_time": bot["start_time"]
        }
        
    def stop_bot(self, bot_id: str) -> Dict[str, Any]:
        """
        Stop a running bot
        
        Args:
            bot_id: ID of the bot to stop
            
        Returns:
            Dictionary with stop result
        """
        if bot_id not in self.active_bots:
            return {"error": f"Bot with ID {bot_id} not found"}
            
        bot = self.active_bots[bot_id]
        
        if bot["status"] != "running":
            return {"error": f"Bot with ID {bot_id} is not running"}
            
        # Set stop flag for the bot thread
        bot["stop_flag"] = True
        
        # Wait for thread to finish (with timeout)
        if bot["thread"] and bot["thread"].is_alive():
            bot["thread"].join(timeout=5.0)
            
        bot["status"] = "stopped"
        bot["stop_time"] = datetime.now().isoformat()
        
        # Calculate run duration
        if "start_time" in bot:
            start_time = datetime.fromisoformat(bot["start_time"])
            stop_time = datetime.fromisoformat(bot["stop_time"])
            duration = (stop_time - start_time).total_seconds()
            bot["run_duration"] = duration
            
        return {
            "bot_id": bot_id,
            "type": bot["type"],
            "status": "stopped",
            "stop_time": bot["stop_time"],
            "run_duration": bot.get("run_duration")
        }
        
    def get_bot_status(self, bot_id: str) -> Dict[str, Any]:
        """
        Get the current status and results of a bot
        
        Args:
            bot_id: ID of the bot
            
        Returns:
            Dictionary with bot status and results
        """
        if bot_id not in self.active_bots:
            return {"error": f"Bot with ID {bot_id} not found"}
            
        bot = self.active_bots[bot_id]
        
        # Create a copy of the bot config without the thread object
        status = {k: v for k, v in bot.items() if k != "thread"}
        
        return status
        
    def list_bots(self, bot_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all active bots, optionally filtered by type
        
        Args:
            bot_type: Optional type to filter by
            
        Returns:
            List of bot information dictionaries
        """
        result = []
        
        for bot_id, bot in self.active_bots.items():
            if bot_type and bot["type"] != bot_type:
                continue
                
            # Create a summary without the thread object and detailed logs
            summary = {
                "id": bot["id"],
                "type": bot["type"],
                "status": bot["status"],
                "created_at": bot["created_at"]
            }
            
            if "start_time" in bot:
                summary["start_time"] = bot["start_time"]
                
            if "stop_time" in bot:
                summary["stop_time"] = bot["stop_time"]
                
            # Add type-specific information
            if bot["type"] == "web_crawler":
                summary["urls_visited"] = len(bot.get("visited_urls", []))
                summary["content_found"] = len(bot.get("found_content", []))
                
            elif bot["type"] == "social_media_bot":
                summary["platform"] = bot.get("platform")
                summary["activities"] = len(bot.get("activity_log", []))
                
            result.append(summary)
            
        return result
        
    def delete_bot(self, bot_id: str) -> Dict[str, Any]:
        """
        Delete a bot and its data
        
        Args:
            bot_id: ID of the bot to delete
            
        Returns:
            Dictionary with deletion result
        """
        if bot_id not in self.active_bots:
            return {"error": f"Bot with ID {bot_id} not found"}
            
        bot = self.active_bots[bot_id]
        
        # Stop the bot if it's running
        if bot["status"] == "running":
            self.stop_bot(bot_id)
            
        # Remove the bot
        del self.active_bots[bot_id]
        
        return {
            "success": True,
            "message": f"Bot {bot_id} deleted"
        }
        
    # Bot implementation methods
    def _run_web_crawler_bot(self, bot_id: str) -> None:
        """
        Run a web crawler bot (backend implementation)
        
        Args:
            bot_id: ID of the bot to run
        """
        bot = self.active_bots[bot_id]
        bot["stop_flag"] = False
        bot["visited_urls"] = []
        bot["found_content"] = []
        bot["queue"] = []
        
        # Initialize the queue with start URLs
        for url in bot["start_urls"]:
            bot["queue"].append((url, 0))  # (URL, depth)
            
        session = None
        
        try:
            # Set up the requests session
            if bot["use_tor"] and self.tor_manager:
                session = self.tor_manager._get_tor_session()
            else:
                session = requests.Session()
                
            # Set the user agent
            session.headers.update({"User-Agent": bot["user_agent"]})
            
            while bot["queue"] and len(bot["visited_urls"]) < bot["max_pages"] and not bot.get("stop_flag", False):
                current_url, depth = bot["queue"].pop(0)
                
                # Skip if already visited
                if current_url in bot["visited_urls"]:
                    continue
                    
                # Add to visited list
                bot["visited_urls"].append(current_url)
                
                try:
                    # Random delay between requests
                    delay = random.uniform(bot["delay_range"][0], bot["delay_range"][1])
                    time.sleep(delay)
                    
                    # Make the request
                    response = session.get(current_url, timeout=10)
                    
                    # Process the response
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        
                        # Check for keywords in content
                        if bot["keywords"]:
                            page_text = soup.get_text().lower()
                            for keyword in bot["keywords"]:
                                if keyword.lower() in page_text:
                                    bot["found_content"].append({
                                        "url": current_url,
                                        "keyword": keyword,
                                        "timestamp": datetime.now().isoformat()
                                    })
                                    
                        # Extract links if not at max depth
                        if depth < bot["max_depth"]:
                            links = soup.find_all("a", href=True)
                            for link in links:
                                href = link["href"]
                                
                                # Handle relative URLs
                                if href.startswith("/"):
                                    from urllib.parse import urlparse
                                    parsed_url = urlparse(current_url)
                                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                                    href = base_url + href
                                    
                                # Skip non-HTTP links
                                if not href.startswith(("http://", "https://")):
                                    continue
                                    
                                # Add to queue if not already visited
                                if href not in bot["visited_urls"] and href not in [url for url, _ in bot["queue"]]:
                                    bot["queue"].append((href, depth + 1))
                                    
                except Exception as e:
                    logger.error(f"Error crawling {current_url}: {str(e)}")
                    if "errors" not in bot:
                        bot["errors"] = []
                    bot["errors"].append({
                        "url": current_url,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    })
                    
        except Exception as e:
            logger.error(f"Web crawler bot error: {str(e)}")
            bot["error"] = str(e)
            
        finally:
            bot["status"] = "completed"
            bot["end_time"] = datetime.now().isoformat()
            
    def _run_chat_bot(self, bot_id: str) -> None:
        """
        Run a chat bot (backend implementation)
        
        Args:
            bot_id: ID of the bot to run
        """
        bot = self.active_bots[bot_id]
        bot["stop_flag"] = False
        bot["log"] = []
        
        # In a real implementation, this would integrate with chat platform APIs
        # For demonstration, we'll simulate chat interactions
        
        try:
            # Simulated chat loop
            for i in range(10):  # Simulate 10 chat interactions
                if bot.get("stop_flag", False):
                    break
                    
                # Simulate a delay between messages
                time.sleep(random.uniform(1.0, 3.0))
                
                # Simulated incoming message
                incoming_message = {
                    "sender": f"user_{random.randint(1000, 9999)}",
                    "content": f"Test message {i+1}",
                    "timestamp": datetime.now().isoformat()
                }
                
                # Log the incoming message
                bot["log"].append({
                    "direction": "incoming",
                    "message": incoming_message,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Simulate processing time
                time.sleep(0.5)
                
                # Simulated bot response
                response = {
                    "content": f"Bot response to message {i+1}",
                    "timestamp": datetime.now().isoformat()
                }
                
                # Log the outgoing message
                bot["log"].append({
                    "direction": "outgoing",
                    "message": response,
                    "timestamp": datetime.now().isoformat()
                })
                
        except Exception as e:
            logger.error(f"Chat bot error: {str(e)}")
            bot["error"] = str(e)
            
        finally:
            bot["status"] = "completed"
            bot["end_time"] = datetime.now().isoformat()
            
    def _run_social_media_bot(self, bot_id: str) -> None:
        """
        Run a social media bot (backend implementation)
        
        Args:
            bot_id: ID of the bot to run
        """
        bot = self.active_bots[bot_id]
        bot["stop_flag"] = False
        bot["activity_log"] = []
        
        # In a real implementation, this would integrate with social media platform APIs
        # For demonstration, we'll simulate social media activities
        
        try:
            # Simulated activity loop
            for i in range(5):  # Simulate 5 social media activities
                if bot.get("stop_flag", False):
                    break
                    
                # Simulate a delay between activities
                time.sleep(random.uniform(2.0, 5.0))
                
                # Random activity type
                activity_type = random.choice(["post", "like", "comment", "follow"])
                
                # Simulated activity
                activity = {
                    "type": activity_type,
                    "target": f"user_{random.randint(1000, 9999)}",
                    "content": f"Test content for activity {i+1}" if activity_type in ["post", "comment"] else None,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Log the activity
                bot["activity_log"].append(activity)
                
        except Exception as e:
            logger.error(f"Social media bot error: {str(e)}")
            bot["error"] = str(e)
            
        finally:
            bot["status"] = "completed"
            bot["end_time"] = datetime.now().isoformat()
            
    def _run_ddos_simulator(self, bot_id: str) -> None:
        """
        Run a DDoS simulator bot (backend implementation)
        
        Args:
            bot_id: ID of the bot to run
        """
        bot = self.active_bots[bot_id]
        bot["stop_flag"] = False
        bot["stats"] = {
            "requests_sent": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat()
        }
        
        # This is a simulated implementation for educational purposes only
        # No actual traffic is generated
        
        try:
            # Simulated DDoS loop
            start_time = time.time()
            end_time = start_time + bot["duration"]
            
            while time.time() < end_time and not bot.get("stop_flag", False):
                # Simulate request attempts based on rate
                for _ in range(bot["rate"]):
                    # Simulate a request attempt
                    success = random.random() > 0.2  # 80% success rate in simulation
                    
                    if success:
                        bot["stats"]["requests_sent"] += 1
                    else:
                        bot["stats"]["errors"] += 1
                        
                # Sleep for 1 second before the next batch
                time.sleep(1.0)
                
            # Update final stats
            bot["stats"]["end_time"] = datetime.now().isoformat()
            bot["stats"]["duration"] = time.time() - start_time
            
        except Exception as e:
            logger.error(f"DDoS simulator error: {str(e)}")
            bot["error"] = str(e)
            
        finally:
            bot["status"] = "completed"
            bot["end_time"] = datetime.now().isoformat()
            
    def add_user_task(self, bot_id: str, task_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a user-defined task to be performed by a bot
        
        Args:
            bot_id: ID of the bot to perform the task
            task_type: Type of task (e.g., "post", "search", "message", "scan")
            task_data: Task-specific data
            
        Returns:
            Dictionary with task addition result
        """
        if bot_id not in self.active_bots:
            return {"error": f"Bot with ID {bot_id} not found"}
        
        bot = self.active_bots[bot_id]
        task_id = f"task_{int(time.time())}_{random.randint(1000, 9999)}"
        
        task = {
            "id": task_id,
            "type": task_type,
            "data": task_data,
            "status": "queued",
            "created_at": datetime.now().isoformat(),
            "result": None
        }
        
        # Initialize task queue if it doesn't exist
        if bot_id not in self.task_queue:
            self.task_queue[bot_id] = []
            
        # Add task to queue
        self.task_queue[bot_id].append(task)
        
        return {
            "task_id": task_id,
            "status": "queued",
            "message": f"Task added to queue for bot {bot_id}"
        }
    
    def execute_user_task(self, bot_id: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a specific task or the next task in queue
        
        Args:
            bot_id: ID of the bot to execute the task
            task_id: Optional ID of specific task to execute
            
        Returns:
            Dictionary with task execution result
        """
        if bot_id not in self.active_bots:
            return {"error": f"Bot with ID {bot_id} not found"}
            
        if bot_id not in self.task_queue or not self.task_queue[bot_id]:
            return {"error": "No tasks in queue for this bot"}
            
        bot = self.active_bots[bot_id]
        
        # Find the task to execute
        task_to_execute = None
        if task_id:
            for task in self.task_queue[bot_id]:
                if task["id"] == task_id:
                    task_to_execute = task
                    break
            if not task_to_execute:
                return {"error": f"Task with ID {task_id} not found"}
        else:
            # Get the first queued task
            for task in self.task_queue[bot_id]:
                if task["status"] == "queued":
                    task_to_execute = task
                    break
                    
        if not task_to_execute:
            return {"error": "No queued tasks found"}
            
        # Update task status
        task_to_execute["status"] = "executing"
        task_to_execute["start_time"] = datetime.now().isoformat()
        
        # Execute task based on bot type and task type
        result = self._execute_bot_task(bot_id, task_to_execute)
        
        # Update task with result
        task_to_execute["status"] = "completed"
        task_to_execute["end_time"] = datetime.now().isoformat()
        task_to_execute["result"] = result
        
        return {
            "task_id": task_to_execute["id"],
            "status": "completed",
            "result": result
        }
    
    def _execute_bot_task(self, bot_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific task for a bot
        
        Args:
            bot_id: ID of the bot
            task: Task configuration dictionary
            
        Returns:
            Dictionary with task result
        """
        bot = self.active_bots[bot_id]
        task_type = task["type"]
        task_data = task["data"]
        bot_type = bot["type"]
        
        # Web crawler bot tasks
        if bot_type == "web_crawler":
            if task_type == "search":
                # Search for content on specific URLs
                return self._crawler_search_task(bot_id, task_data)
            elif task_type == "download":
                # Download content from a URL
                return self._crawler_download_task(bot_id, task_data)
            elif task_type == "extract":
                # Extract specific data from previously crawled pages
                return self._crawler_extract_task(bot_id, task_data)
                
        # Chat bot tasks
        elif bot_type == "chat_bot":
            if task_type == "message":
                # Send a message to a specific channel/user
                return self._chat_message_task(bot_id, task_data)
            elif task_type == "listen":
                # Listen for messages matching criteria
                return self._chat_listen_task(bot_id, task_data)
                
        # Social media bot tasks
        elif bot_type == "social_media_bot":
            if task_type == "post":
                # Create a post on social media
                return self._social_post_task(bot_id, task_data)
            elif task_type == "interact":
                # Interact with existing content (like, comment, share)
                return self._social_interact_task(bot_id, task_data)
            elif task_type == "follow":
                # Follow users based on criteria
                return self._social_follow_task(bot_id, task_data)
                
        # Network scanner bot tasks
        elif bot_type == "network_scanner":
            if task_type == "scan_target":
                # Scan a specific target
                return self._scanner_scan_target_task(bot_id, task_data)
            elif task_type == "analyze_results":
                # Analyze scan results
                return self._scanner_analyze_results_task(bot_id, task_data)
        
        # If no matching task type was found
        return {
            "error": f"Unsupported task type '{task_type}' for bot type '{bot_type}'",
            "status": "failed"
        }
    
    def _crawler_search_task(self, bot_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a search task with a web crawler bot"""
        bot = self.active_bots[bot_id]
        urls = task_data.get("urls", [])
        keywords = task_data.get("keywords", [])
        max_pages = task_data.get("max_pages", 10)
        
        results = []
        visited = 0
        matches = 0
        
        # Create a session for requests
        session = requests.Session()
        session.headers.update({"User-Agent": bot["user_agent"]})
        
        for url in urls[:max_pages]:
            try:
                response = session.get(url, timeout=10)
                visited += 1
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    text_content = soup.get_text().lower()
                    
                    found_keywords = []
                    for keyword in keywords:
                        if keyword.lower() in text_content:
                            found_keywords.append(keyword)
                            matches += 1
                    
                    if found_keywords:
                        results.append({
                            "url": url,
                            "keywords_found": found_keywords,
                            "title": soup.title.text if soup.title else "No title"
                        })
                
                # Small delay between requests
                time.sleep(random.uniform(1.0, 3.0))
                
            except Exception as e:
                logger.error(f"Error searching URL {url}: {str(e)}")
        
        return {
            "status": "success",
            "pages_visited": visited,
            "matches_found": matches,
            "results": results
        }
    
    def _crawler_download_task(self, bot_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Download content from a URL with a web crawler bot"""
        url = task_data.get("url")
        save_html = task_data.get("save_html", True)
        save_text = task_data.get("save_text", True)
        save_images = task_data.get("save_images", False)
        
        if not url:
            return {"error": "No URL provided for download task"}
        
        try:
            response = requests.get(url, timeout=15)
            
            if response.status_code != 200:
                return {
                    "error": f"Failed to download: HTTP {response.status_code}",
                    "url": url
                }
            
            result = {
                "url": url,
                "content_type": response.headers.get("Content-Type", "unknown"),
                "size_bytes": len(response.content),
                "download_time": datetime.now().isoformat()
            }
            
            if save_html and "text/html" in response.headers.get("Content-Type", ""):
                result["html"] = response.text[:10000] + "..." if len(response.text) > 10000 else response.text
            
            if save_text and "text/html" in response.headers.get("Content-Type", ""):
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(separator="\n", strip=True)
                result["text"] = text[:5000] + "..." if len(text) > 5000 else text
            
            if save_images and "text/html" in response.headers.get("Content-Type", ""):
                soup = BeautifulSoup(response.text, "html.parser")
                images = []
                for img in soup.find_all("img", src=True):
                    images.append(img["src"])
                result["images"] = images[:20]  # Limit to first 20 images
            
            return {
                "status": "success",
                "download_result": result
            }
            
        except Exception as e:
            logger.error(f"Error downloading {url}: {str(e)}")
            return {
                "error": str(e),
                "url": url,
                "status": "failed"
            }
    
    def _crawler_extract_task(self, bot_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract specific data from previously crawled pages"""
        bot = self.active_bots[bot_id]
        selectors = task_data.get("selectors", {})
        url_pattern = task_data.get("url_pattern", "")
        max_results = task_data.get("max_results", 10)
        
        matches = []
        processed = 0
        
        # Find matching URLs from previously crawled pages
        matching_urls = []
        for url in bot.get("visited_urls", []):
            if not url_pattern or url_pattern in url:
                matching_urls.append(url)
        
        # Limit to max_results
        matching_urls = matching_urls[:max_results]
        
        # Create a session for requests
        session = requests.Session()
        session.headers.update({"User-Agent": bot["user_agent"]})
        
        for url in matching_urls:
            try:
                response = session.get(url, timeout=10)
                processed += 1
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    result = {"url": url, "extracted_data": {}}
                    
                    # Apply each selector and extract data
                    for name, selector in selectors.items():
                        elements = soup.select(selector)
                        if elements:
                            result["extracted_data"][name] = [elem.get_text(strip=True) for elem in elements]
                    
                    if result["extracted_data"]:
                        matches.append(result)
                
                # Small delay between requests
                time.sleep(random.uniform(1.0, 2.0))
                
            except Exception as e:
                logger.error(f"Error extracting from {url}: {str(e)}")
        
        return {
            "status": "success",
            "pages_processed": processed,
            "matches_found": len(matches),
            "results": matches
        }
    
    def _chat_message_task(self, bot_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message with a chat bot"""
        recipient = task_data.get("recipient")
        message = task_data.get("message")
        
        if not recipient or not message:
            return {"error": "Missing recipient or message"}
        
        # In a real implementation, this would use platform-specific APIs
        # For demonstration, we'll simulate sending a message
        
        return {
            "status": "success",
            "recipient": recipient,
            "message_preview": message[:50] + "..." if len(message) > 50 else message,
            "timestamp": datetime.now().isoformat()
        }
    
    def _chat_listen_task(self, bot_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Listen for messages matching criteria"""
        keywords = task_data.get("keywords", [])
        channels = task_data.get("channels", [])
        duration = min(task_data.get("duration", 60), 300)  # Max 5 minutes
        
        # In a real implementation, this would use platform-specific APIs
        # For demonstration, we'll simulate listening for messages
        
        # Simulate finding messages
        found_messages = []
        for _ in range(random.randint(0, 5)):
            channel = random.choice(channels) if channels else f"channel_{random.randint(1000, 9999)}"
            sender = f"user_{random.randint(1000, 9999)}"
            keyword = random.choice(keywords) if keywords else None
            
            message_text = f"This is a simulated message"
            if keyword:
                message_text += f" containing the keyword '{keyword}'"
            
            found_messages.append({
                "channel": channel,
                "sender": sender,
                "message": message_text,
                "timestamp": datetime.now().isoformat()
            })
        
        return {
            "status": "success",
            "listened_duration": duration,
            "channels_monitored": len(channels),
            "messages_found": len(found_messages),
            "matching_messages": found_messages
        }
    
    def _social_post_task(self, bot_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a post on social media"""
        content = task_data.get("content")
        platform = task_data.get("platform", "custom")
        
        if not content:
            return {"error": "No content provided for post"}
        
        # In a real implementation, this would use platform-specific APIs
        # For demonstration, we'll simulate posting
        
        return {
            "status": "success",
            "platform": platform,
            "content_preview": content[:50] + "..." if len(content) > 50 else content,
            "post_id": f"post_{random.randint(10000, 99999)}",
            "timestamp": datetime.now().isoformat()
        }
    
    def _social_interact_task(self, bot_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Interact with existing content on social media"""
        action = task_data.get("action", "like")  # like, comment, share
        target_post = task_data.get("target_post")
        comment_text = task_data.get("comment_text")
        
        if not target_post:
            return {"error": "No target post specified"}
        
        if action == "comment" and not comment_text:
            return {"error": "Comment action requires comment_text"}
        
        # In a real implementation, this would use platform-specific APIs
        # For demonstration, we'll simulate the interaction
        
        return {
            "status": "success",
            "action": action,
            "target_post": target_post,
            "interaction_id": f"interaction_{random.randint(10000, 99999)}",
            "timestamp": datetime.now().isoformat()
        }
    
    def _social_follow_task(self, bot_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Follow users based on criteria"""
        criteria = task_data.get("criteria", {})
        max_users = min(task_data.get("max_users", 5), 20)  # Cap at 20
        
        # In a real implementation, this would use platform-specific APIs
        # For demonstration, we'll simulate following users
        
        followed_users = []
        for i in range(random.randint(1, max_users)):
            username = f"user_{random.randint(1000, 9999)}"
            followed_users.append({
                "username": username,
                "followed_at": datetime.now().isoformat()
            })
        
        return {
            "status": "success",
            "criteria_used": criteria,
            "users_followed": followed_users,
            "total_followed": len(followed_users)
        }
    
    def _scanner_scan_target_task(self, bot_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Scan a specific target with a network scanner bot"""
        target = task_data.get("target")
        scan_type = task_data.get("scan_type", "port_scan")
        ports = task_data.get("ports", [80, 443, 22, 21])
        
        if not target:
            return {"error": "No target specified"}
        
        # In a real implementation, this would perform actual scanning
        # For demonstration, we'll simulate scanning
        
        open_ports = []
        for port in ports:
            if random.random() < 0.3:  # 30% chance port is "open"
                open_ports.append(port)
        
        scan_results = {
            "target": target,
            "scan_type": scan_type,
            "timestamp": datetime.now().isoformat(),
            "open_ports": open_ports
        }
        
        # Add scan-type specific results
        if scan_type == "service_detection" and open_ports:
            scan_results["services"] = {}
            service_map = {
                21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 
                25: "SMTP", 110: "POP3", 143: "IMAP"
            }
            for port in open_ports:
                scan_results["services"][port] = service_map.get(port, "Unknown")
        
        return {
            "status": "success",
            "scan_results": scan_results
        }
    
    def _scanner_analyze_results_task(self, bot_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze scan results for vulnerabilities"""
        scan_id = task_data.get("scan_id")
        
        if not scan_id:
            return {"error": "No scan_id specified for analysis"}
        
        # In a real implementation, this would analyze actual scan results
        # For demonstration, we'll simulate vulnerability analysis
        
        vulnerabilities = []
        if random.random() < 0.4:  # 40% chance to find vulnerabilities
            vuln_types = [
                {"name": "Outdated software", "severity": "Medium"},
                {"name": "Weak encryption", "severity": "Medium"},
                {"name": "Open sensitive port", "severity": "High"},
                {"name": "Default credentials", "severity": "Critical"}
            ]
            
            for _ in range(random.randint(1, 3)):
                vuln = random.choice(vuln_types)
                vulnerabilities.append({
                    "type": vuln["name"],
                    "severity": vuln["severity"],
                    "description": f"Simulated {vuln['name']} vulnerability",
                    "fix_recommendation": f"Update software and secure configuration"
                })
        
        return {
            "status": "success",
            "scan_id": scan_id,
            "vulnerabilities_found": len(vulnerabilities),
            "vulnerabilities": vulnerabilities,
            "analysis_timestamp": datetime.now().isoformat()
        }

    def _run_network_scanner(self, bot_id: str) -> None:
        """
        Run a network scanner bot (backend implementation)
        
        Args:
            bot_id: ID of the bot to run
        """
        bot = self.active_bots[bot_id]
        bot["stop_flag"] = False
        bot["results"] = {
            "open_ports": [],
            "services": {},
            "os_info": None,
            "vulnerabilities": []
        }
        
        try:
            target = bot["target"]
            scan_type = bot["scan_type"]
            port_range = bot["port_range"]
            
            # Simple port scan implementation
            if scan_type in ["port_scan", "service_detection"]:
                for port in port_range:
                    if bot.get("stop_flag", False):
                        break
                        
                    try:
                        # Create a socket and attempt to connect
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1.0)
                        result = sock.connect_ex((target, port))
                        sock.close()
                        
                        # If port is open
                        if result == 0:
                            bot["results"]["open_ports"].append(port)
                            
                            # Simulate service detection
                            if scan_type == "service_detection":
                                # In a real implementation, this would use techniques like banner grabbing
                                # For demonstration, we'll use a simple mapping
                                service_map = {
                                    21: "FTP",
                                    22: "SSH",
                                    23: "Telnet",
                                    25: "SMTP",
                                    53: "DNS",
                                    80: "HTTP",
                                    110: "POP3",
                                    443: "HTTPS",
                                    3306: "MySQL",
                                    3389: "RDP"
                                }
                                if port in service_map:
                                    bot["results"]["services"][port] = service_map[port]
                                else:
                                    bot["results"]["services"][port] = "Unknown"
                        
                        # Add a small delay between port checks
                        time.sleep(0.1)
                        
                    except socket.error:
                        pass
                        
            # Simulate OS detection (in a real implementation, this would use techniques like TCP/IP stack fingerprinting)
            if scan_type == "os_detection":
                # Simulate OS detection result
                os_options = ["Windows 10", "Ubuntu 20.04", "CentOS 8", "macOS 11.4", "Unknown"]
                bot["results"]["os_info"] = {
                    "os": random.choice(os_options),
                    "confidence": random.randint(70, 95),
                    "method": "Simulated"
                }
                
            # Simulate vulnerability scan (in a real implementation, this would check for known vulnerabilities)
            if scan_type == "vulnerability_scan":
                # Simulate vulnerability findings based on open ports
                for port in bot["results"]["open_ports"]:
                    if port == 21:
                        bot["results"]["vulnerabilities"].append({
                            "port": port,
                            "service": "FTP",
                            "vulnerability": "Anonymous FTP access",
                            "severity": "Medium",
                            "description": "FTP server allows anonymous access"
                        })
                    elif port == 23:
                        bot["results"]["vulnerabilities"].append({
                            "port": port,
                            "service": "Telnet",
                            "vulnerability": "Telnet cleartext communication",
                            "severity": "High",
                            "description": "Telnet transmits data in cleartext, including credentials"
                        })
                        
        except Exception as e:
            logger.error(f"Network scanner error: {str(e)}")
            bot["error"] = str(e)
            
        finally:
            bot["status"] = "completed"
            bot["end_time"] = datetime.now().isoformat()
            
    def _run_crypto_miner_sim(self, bot_id: str) -> None:
        """
        Run a cryptocurrency miner simulation (backend implementation)
        
        Args:
            bot_id: ID of the bot to run
        """
        bot = self.active_bots[bot_id]
        bot["stop_flag"] = False
        bot["mining_statistics"]["start_time"] = datetime.now().isoformat()
        
        try:
            # Simulated mining loop
            while not bot.get("stop_flag", False):
                # Update simulated mining statistics
                bot["mining_statistics"]["hash_rate"] = f"{random.randint(10, 1000)} H/s"
                
                # Simulate finding a block (very low probability)
                if random.random() < 0.01:  # 1% chance per iteration
                    bot["mining_statistics"]["blocks_found"] += 1
                    
                # Update estimated earnings based on network
                if bot["network"] == "bitcoin":
                    bot["mining_statistics"]["estimated_earnings"] = bot["mining_statistics"]["blocks_found"] * 6.25
                elif bot["network"] == "ethereum":
                    bot["mining_statistics"]["estimated_earnings"] = bot["mining_statistics"]["blocks_found"] * 2.0
                elif bot["network"] == "monero":
                    bot["mining_statistics"]["estimated_earnings"] = bot["mining_statistics"]["blocks_found"] * 1.5
                elif bot["network"] == "litecoin":
                    bot["mining_statistics"]["estimated_earnings"] = bot["mining_statistics"]["blocks_found"] * 12.5
                    
                # Sleep for a bit
                time.sleep(1.0)
                
        except Exception as e:
            logger.error(f"Crypto miner sim error: {str(e)}")
            bot["error"] = str(e)
            
        finally:
            bot["status"] = "completed"
            bot["mining_statistics"]["end_time"] = datetime.now().isoformat()
            bot["end_time"] = datetime.now().isoformat()