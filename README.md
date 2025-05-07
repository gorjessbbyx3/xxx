# BINGOxBANGO

## Advanced Dark Web Crawler with Security Tools

BINGOxBANGO is a comprehensive cybersecurity platform featuring dark web crawling capabilities with integrated AI analysis and a suite of interactive security tools.

## Key Features

### Dark Web Crawler
- Multi-level traversal of .onion sites
- Content extraction and analysis
- AI-powered content categorization
- Automated crawling with depth control

### Security Tools
- Vulnerability Scanner: Identify security weaknesses in websites and network services
- Location Changer: Route traffic through Tor for anonymized connections
- Email Templates: Generate templates for security awareness training and phishing simulations
- Bot Maker: Create automated agents for security testing and data collection

### AI Integration
- Content analysis using local Mistral 7B model via Ollama
- Entity extraction from dark web content
- Risk assessment of crawled sites
- Automated report generation

## Requirements

- Python 3.9+
- Tor service
- Ollama (for AI capabilities)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```
git clone https://github.com/gorjessbbyx3/BINGOxBANGO.git
cd BINGOxBANGO
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Install and configure Tor:
```
# On Debian/Ubuntu
sudo apt install tor
sudo systemctl start tor
```

4. Install Ollama and download the required model:
```
# Follow instructions at https://ollama.ai/
ollama pull mistral:7b
```

## Usage

1. Start the web interface:
```
python app/routes.py
```

2. Access the dashboard at http://localhost:5000

3. Use CLI for specific operations:
```
python cli.py status
```

## Warning

This tool is intended for legal security research and testing only. Always obtain proper authorization before scanning or crawling any website. The authors are not responsible for any misuse of this software.

## License

This project is licensed under the MIT License - see the LICENSE file for details.