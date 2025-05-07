"""
AI Analyzer - Handles communication with AI models for content analysis
Supports Ollama locally and OpenAI API for deployment
"""
import json
import logging
import requests
import time
import os
from typing import Dict, Any, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ai_analyzer')

class OllamaAnalyzer:
    """
    Class to handle interactions with AI models for analysis
    Supports Ollama locally and OpenAI API for deployment
    """
    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "ghosttrace"):
        """
        Initialize the AI Analyzer with the appropriate configuration
        """
        self.base_url = base_url
        self.model_name = model_name
        self.api_url = f"{base_url}/api"
        self.use_openai = False
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        # If OPENAI_API_KEY is set, use OpenAI instead of Ollama
        if self.openai_api_key:
            self.use_openai = True
            logger.info("Using OpenAI API for analysis")
        else:
            logger.info(f"Ollama Analyzer initialized with model: {model_name}")
        
    def check_model_availability(self) -> bool:
        """
        Check if the specified model is available in Ollama or if OpenAI is configured
        """
        # If using OpenAI, just check if API key is present
        if self.use_openai:
            if self.openai_api_key:
                logger.info("OpenAI API key found, ready to use OpenAI models")
                return True
            else:
                logger.error("OpenAI API key not found but use_openai is set")
                return False
        
        # Otherwise check Ollama
        try:
            response = requests.get(f"{self.api_url}/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                for model in models:
                    if model.get("name") == self.model_name:
                        logger.info(f"Model {self.model_name} is available")
                        return True
                logger.warning(f"Model {self.model_name} not found, falling back to mistral:7b-instruct")
                self.model_name = "mistral:7b-instruct"
                return self.check_model_availability()
            else:
                logger.error(f"Failed to get model list: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False
    
    def analyze_content(self, content: str, prompt_template: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze the provided content using Ollama or OpenAI
        
        Args:
            content: The dark web content to analyze
            prompt_template: Optional template for the prompt
            
        Returns:
            Dictionary with analysis results
        """
        if not prompt_template:
            prompt_template = """
You are GhostTrace, a specialized analyst focusing on dark web content.
Analyze the following content from a dark web page and provide a detailed report that includes:

1. Summary of the content
2. Identified topics and themes
3. Potential illegal activities mentioned
4. Key entities (people, organizations, locations)
5. Risk assessment (low, medium, high)
6. Recommendations for further investigation

Content to analyze:
{content}

Provide your analysis in a structured format.
"""
        
        prompt = prompt_template.format(content=content)
        
        # Check if we should use OpenAI
        if self.use_openai:
            try:
                # If OpenAI package is installed
                try:
                    import openai
                    
                    # Initialize OpenAI client
                    openai_client = openai.OpenAI(api_key=self.openai_api_key)
                    
                    logger.info(f"Sending analysis request to OpenAI for content of length {len(content)}")
                    response = openai_client.chat.completions.create(
                        model="gpt-4o",  # Use the latest model
                        messages=[
                            {"role": "system", "content": "You are GhostTrace, a specialized dark web content analyzer."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1000
                    )
                    
                    # Extract response
                    result = response.choices[0].message.content
                    
                    logger.info("OpenAI analysis completed successfully")
                    return {
                        "success": True,
                        "analysis": result,
                        "metrics": {
                            "tokens": response.usage.total_tokens,
                            "model": "gpt-4o"
                        }
                    }
                
                except ImportError:
                    # OpenAI package not installed, use direct API call
                    import json
                    
                    logger.info("OpenAI package not installed, using direct API call")
                    api_url = "https://api.openai.com/v1/chat/completions"
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.openai_api_key}"
                    }
                    data = {
                        "model": "gpt-4o",
                        "messages": [
                            {"role": "system", "content": "You are GhostTrace, a specialized dark web content analyzer."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 1000
                    }
                    
                    response = requests.post(api_url, headers=headers, json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        analysis = result["choices"][0]["message"]["content"]
                        
                        logger.info("OpenAI direct API analysis completed successfully")
                        return {
                            "success": True,
                            "analysis": analysis,
                            "metrics": {
                                "tokens": result["usage"]["total_tokens"],
                                "model": "gpt-4o"
                            }
                        }
                    else:
                        error_msg = f"Failed to analyze with OpenAI API: {response.status_code} - {response.text}"
                        logger.error(error_msg)
                        return {
                            "success": False,
                            "error": error_msg
                        }
                        
            except Exception as e:
                error_msg = f"Error during OpenAI content analysis: {str(e)}"
                logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg
                }
        
        # Otherwise use Ollama
        try:
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            logger.info(f"Sending analysis request to Ollama for content of length {len(content)}")
            response = requests.post(f"{self.api_url}/generate", json=data)
            
            if response.status_code == 200:
                result = response.json()
                logger.info("Analysis completed successfully")
                return {
                    "success": True,
                    "analysis": result.get("response", ""),
                    "metrics": {
                        "eval_count": result.get("eval_count", 0),
                        "eval_duration": result.get("eval_duration", 0)
                    }
                }
            else:
                error_msg = f"Failed to analyze content: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg
                }
        except Exception as e:
            error_msg = f"Error during content analysis: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    def extract_entities(self, content: str) -> Dict[str, List[str]]:
        """
        Extract named entities from the content
        
        Args:
            content: Text to analyze for entities
            
        Returns:
            Dictionary with entity types and lists of entities
        """
        prompt = """
Extract all named entities from the following dark web content. 
Categorize entities into these types: PERSON, ORGANIZATION, LOCATION, CRYPTOCURRENCY, EMAIL, URL, PHONE_NUMBER, DATE, PRODUCT.
For each entity type, provide a list of all unique entities found.

Content:
{content}

Format your response as a structured JSON object with entity types as keys and arrays of unique entities as values.
Only return the JSON object, nothing else.
"""
        
        result = self.analyze_content(content, prompt_template=prompt)
        
        if result["success"]:
            try:
                # Try to extract JSON from the response
                analysis_text = result["analysis"]
                
                # Look for JSON object in the response
                json_start = analysis_text.find('{')
                json_end = analysis_text.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = analysis_text[json_start:json_end]
                    entities = json.loads(json_str)
                    return entities
                
                # If no JSON found, return empty entity dict
                logger.warning("No valid JSON found in entity extraction response")
                return {
                    "PERSON": [],
                    "ORGANIZATION": [],
                    "LOCATION": [],
                    "CRYPTOCURRENCY": [],
                    "EMAIL": [],
                    "URL": [],
                    "PHONE_NUMBER": [],
                    "DATE": [],
                    "PRODUCT": []
                }
            except json.JSONDecodeError:
                logger.error("Failed to parse entity extraction result as JSON")
                # Return empty data structure to maintain type compatibility
                return {
                    "PERSON": [],
                    "ORGANIZATION": [],
                    "LOCATION": [],
                    "CRYPTOCURRENCY": [],
                    "EMAIL": [],
                    "URL": [],
                    "PHONE_NUMBER": [],
                    "DATE": [],
                    "PRODUCT": [],
                    "error_message": "Failed to parse entity data"
                }
        else:
            # Return empty data structure with error message
            return {
                "PERSON": [],
                "ORGANIZATION": [],
                "LOCATION": [],
                "CRYPTOCURRENCY": [],
                "EMAIL": [],
                "URL": [],
                "PHONE_NUMBER": [],
                "DATE": [],
                "PRODUCT": [],
                "error_message": result.get("error", "Unknown error in entity extraction")
            }
    
    def categorize_content(self, content: str) -> Dict[str, Any]:
        """
        Categorize the content by topic and risk level
        
        Args:
            content: Text to categorize
            
        Returns:
            Dictionary with categorization results
        """
        prompt = """
Categorize the following dark web content by topic and risk level.

Topics to consider:
- Drugs
- Weapons
- Financial fraud
- Hacking services
- Counterfeit goods
- Personal data
- Illegal services
- Other (specify)

Risk levels:
1 - Low risk: General discussion, theoretical, legal content
2 - Medium risk: Suspicious content, potential illegal activities
3 - High risk: Clearly illegal activities, immediate threats

Content:
{content}

Provide your analysis as a JSON object with these fields:
- primary_topic: The main topic of the content
- secondary_topics: Array of other topics mentioned
- risk_level: Numeric score (1-3)
- risk_explanation: Brief explanation of the risk assessment
- keywords: Array of significant keywords found

Only return the JSON object, nothing else.
"""
        result = self.analyze_content(content, prompt_template=prompt)
        
        if result["success"]:
            try:
                # Try to extract JSON from the response
                analysis_text = result["analysis"]
                
                # Look for JSON object in the response
                json_start = analysis_text.find('{')
                json_end = analysis_text.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = analysis_text[json_start:json_end]
                    categorization = json.loads(json_str)
                    return categorization
                
                # If no JSON found, return text analysis
                logger.warning("No valid JSON found in categorization response")
                return {
                    "primary_topic": "Unknown",
                    "secondary_topics": [],
                    "risk_level": 0,
                    "risk_explanation": "Could not determine risk level",
                    "keywords": [],
                    "raw_analysis": analysis_text
                }
            except json.JSONDecodeError:
                logger.error("Failed to parse categorization result as JSON")
                return {"error": "Failed to parse categorization data", "raw_analysis": result["analysis"]}
        else:
            return {"error": result.get("error", "Unknown error in categorization")}

    def wait_for_ollama(self, max_retries=10, retry_delay=5):
        """
        Wait for Ollama service to be available
        
        Args:
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            
        Returns:
            Boolean indicating if Ollama is available
        """
        logger.info(f"Waiting for Ollama service to be available at {self.api_url}")
        
        for attempt in range(max_retries):
            try:
                response = requests.get(f"{self.api_url}/tags")
                if response.status_code == 200:
                    logger.info("Ollama service is available")
                    return True
                else:
                    logger.warning(f"Attempt {attempt + 1}/{max_retries}: Ollama service returned status {response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1}/{max_retries}: Ollama service not available yet. Error: {e}")
                
            time.sleep(retry_delay)
        
        logger.error(f"Failed to connect to Ollama service after {max_retries} attempts")
        return False
