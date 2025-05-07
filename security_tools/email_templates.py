"""
Email Templates - Templates for creating spam, phishing, and security testing emails
"""
import os
import json
import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailTemplateManager:
    """
    Manager for email templates used in security testing and demonstrations
    """
    def __init__(self, templates_dir: str = "templates/emails"):
        """
        Initialize the email template manager
        
        Args:
            templates_dir: Directory containing email templates
        """
        self.templates_dir = templates_dir
        self.templates = {
            "phishing": [],
            "spam": [],
            "spear_phishing": [],
            "business_email_compromise": [],
            "malware_delivery": []
        }
        self.loaded = False
        
        # Placeholder variables for template customization
        self.variables = {
            "{{FIRST_NAME}}": "Target's first name",
            "{{LAST_NAME}}": "Target's last name",
            "{{FULL_NAME}}": "Target's full name",
            "{{EMAIL}}": "Target's email address",
            "{{COMPANY}}": "Target's company name",
            "{{POSITION}}": "Target's job position",
            "{{DATE}}": datetime.now().strftime("%B %d, %Y"),
            "{{BANK_NAME}}": "Bank name",
            "{{CREDIT_CARD_LAST4}}": "Last 4 digits of credit card",
            "{{TRACKING_NUMBER}}": "Package tracking number",
            "{{ORDER_NUMBER}}": "Order number",
            "{{AMOUNT}}": "Dollar amount",
            "{{SENDER_NAME}}": "Sender's name",
            "{{SENDER_COMPANY}}": "Sender's company",
            "{{SENDER_POSITION}}": "Sender's position",
            "{{URGENT_REASON}}": "Reason for urgency",
            "{{ACCOUNT_ID}}": "Account ID or username",
            "{{WEBSITE}}": "Website name",
            "{{MALICIOUS_LINK}}": "http://definitelynotmalicious.com/login.php",
            "{{YEAR}}": str(datetime.now().year)
        }
    
    def load_templates(self) -> Dict[str, int]:
        """
        Load templates from the templates directory
        
        Returns:
            Dictionary with count of templates loaded by category
        """
        # For demonstration purposes, we'll create predefined templates
        # In a real implementation, these would be loaded from files
        
        # Create the core template structure with built-in templates
        self._initialize_builtin_templates()
        
        # In a real implementation, we would also load from disk:
        # try:
        #     if os.path.exists(self.templates_dir):
        #         for category in self.templates.keys():
        #             category_path = os.path.join(self.templates_dir, category)
        #             if os.path.exists(category_path):
        #                 for filename in os.listdir(category_path):
        #                     if filename.endswith('.json'):
        #                         with open(os.path.join(category_path, filename), 'r') as f:
        #                             template = json.load(f)
        #                             self.templates[category].append(template)
        # except Exception as e:
        #     logger.error(f"Error loading templates: {str(e)}")
        
        self.loaded = True
        
        # Return count of templates by category
        return {category: len(templates) for category, templates in self.templates.items()}
    
    def _initialize_builtin_templates(self) -> None:
        """Initialize the built-in email templates for different categories"""
        
        # Phishing email templates
        self.templates["phishing"] = [
            {
                "name": "Password Reset",
                "subject": "URGENT: Your {{WEBSITE}} password needs to be reset",
                "sender_name": "{{WEBSITE}} Security",
                "sender_email": "security@{{WEBSITE}}.com",
                "body_html": """
                <html>
                <body>
                <p>Dear {{FIRST_NAME}},</p>
                <p>We have detected unusual activity on your {{WEBSITE}} account. To protect your information, your password has been temporarily reset.</p>
                <p>Please click the link below to verify your identity and create a new password:</p>
                <p><a href="{{MALICIOUS_LINK}}">Secure Password Reset</a></p>
                <p>If you do not reset your password within 24 hours, your account may be suspended for security reasons.</p>
                <p>If you did not request this password reset, please ignore this email (but your account may be suspended).</p>
                <p>Thank you,<br>
                {{WEBSITE}} Security Team</p>
                </body>
                </html>
                """,
                "body_text": """
                Dear {{FIRST_NAME}},
                
                We have detected unusual activity on your {{WEBSITE}} account. To protect your information, your password has been temporarily reset.
                
                Please click the link below to verify your identity and create a new password:
                {{MALICIOUS_LINK}}
                
                If you do not reset your password within 24 hours, your account may be suspended for security reasons.
                
                If you did not request this password reset, please ignore this email (but your account may be suspended).
                
                Thank you,
                {{WEBSITE}} Security Team
                """,
                "indicators": [
                    "Urgency to create psychological pressure",
                    "Threat of negative consequences",
                    "Generic greeting",
                    "Suspicious link URL",
                    "Request for credentials"
                ],
                "target_platforms": ["Banking", "Social Media", "Email Providers", "Corporate"]
            },
            {
                "name": "Package Delivery",
                "subject": "Your package {{TRACKING_NUMBER}} could not be delivered",
                "sender_name": "Delivery Notifications",
                "sender_email": "notifications@delivery-updates.com",
                "body_html": """
                <html>
                <body>
                <p>Hello,</p>
                <p>We attempted to deliver your package (Tracking #{{TRACKING_NUMBER}}) today, but were unable to complete the delivery due to:</p>
                <ul>
                <li>Incomplete/incorrect delivery address</li>
                <li>No one available to sign for the package</li>
                <li>Delivery fee unpaid</li>
                </ul>
                <p>To reschedule your delivery, please review and confirm your delivery information by clicking below:</p>
                <p><a href="{{MALICIOUS_LINK}}">Schedule Redelivery</a></p>
                <p>Please note that packages not claimed within 5 days will be returned to sender.</p>
                <p>Thank you for your cooperation.</p>
                </body>
                </html>
                """,
                "body_text": """
                Hello,
                
                We attempted to deliver your package (Tracking #{{TRACKING_NUMBER}}) today, but were unable to complete the delivery due to:
                
                * Incomplete/incorrect delivery address
                * No one available to sign for the package
                * Delivery fee unpaid
                
                To reschedule your delivery, please review and confirm your delivery information by clicking below:
                {{MALICIOUS_LINK}}
                
                Please note that packages not claimed within 5 days will be returned to sender.
                
                Thank you for your cooperation.
                """,
                "indicators": [
                    "Vague sender name",
                    "Suspicious domain",
                    "No specific mention of delivery company",
                    "Urgency with time limit",
                    "Suspicious link"
                ],
                "target_platforms": ["General Public", "E-commerce Customers"]
            },
            {
                "name": "DocuSign Document",
                "subject": "{{SENDER_NAME}} shared a document with you for signature",
                "sender_name": "DocuSign",
                "sender_email": "documents@docusign-alerts.com",
                "body_html": """
                <html>
                <body style="font-family: Arial, sans-serif; color: #333333;">
                <div style="padding: 20px; max-width: 600px; margin: 0 auto;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="https://www.docusign.com/sites/default/files/docusign_logo_0.png" alt="DocuSign" width="180">
                    </div>
                    
                    <div style="border: 1px solid #cccccc; padding: 20px; background-color: #f5f5f5; border-radius: 5px;">
                        <h2 style="color: #2676c0; margin-top: 0;">Please review and sign your document</h2>
                        <p><strong>{{SENDER_NAME}} ({{SENDER_EMAIL}})</strong> has sent you a document to review and sign.</p>
                        
                        <div style="background-color: white; border: 1px solid #ddd; padding: 15px; margin: 20px 0; border-radius: 3px;">
                            <p style="margin-top: 0; font-size: 16px;"><strong>{{DOCUMENT_NAME}}</strong></p>
                            <p>Please review and sign this document by {{EXPIRATION_DATE}}.</p>
                        </div>
                        
                        <div style="text-align: center; margin: 25px 0;">
                            <a href="{{MALICIOUS_LINK}}" style="background-color: #2676c0; color: white; padding: 12px 35px; text-decoration: none; font-weight: bold; border-radius: 5px; font-size: 16px;">REVIEW DOCUMENT</a>
                        </div>
                    </div>
                    
                    <div style="margin-top: 20px; font-size: 12px; color: #666666;">
                        <p>If you believe this email is fraudulent, please forward it to abuse@docusign.com</p>
                        <p>© {{YEAR}} DocuSign Inc. All rights reserved.</p>
                    </div>
                </div>
                </body>
                </html>
                """,
                "body_text": """
                DocuSign
                
                Please review and sign your document
                
                {{SENDER_NAME}} ({{SENDER_EMAIL}}) has sent you a document to review and sign.
                
                {{DOCUMENT_NAME}}
                
                Please review and sign this document by {{EXPIRATION_DATE}}.
                
                REVIEW DOCUMENT: {{MALICIOUS_LINK}}
                
                If you believe this email is fraudulent, please forward it to abuse@docusign.com
                
                © {{YEAR}} DocuSign Inc. All rights reserved.
                """,
                "indicators": [
                    "Slightly off sender email domain",
                    "Legitimate-looking branding and formatting",
                    "Sense of importance and deadline",
                    "Suspicious link URL doesn't match real DocuSign domain",
                    "Social engineering to impersonate trusted brand"
                ],
                "target_platforms": ["Business", "Legal", "Real Estate", "Finance", "Corporate"]
            }
        ]
        
        # Spam email templates
        self.templates["spam"] = [
            {
                "name": "Fake Lottery Win",
                "subject": "CONGRATULATIONS! You've WON $5,000,000.00 USD!!!",
                "sender_name": "International Lottery Commission",
                "sender_email": "claims@int-lottery-commission.org",
                "body_html": """
                <html>
                <body>
                <h1>CONGRATULATIONS!!!</h1>
                <p>Dear Lucky Winner,</p>
                <p>We are pleased to inform you that your email address was randomly selected as the winner of our INTERNATIONAL EMAIL LOTTERY PROGRAM held on {{DATE}}.</p>
                <p>You have been awarded the sum of <b>FIVE MILLION UNITED STATES DOLLARS ($5,000,000.00 USD)</b>.</p>
                <p>To claim your prize, you must contact our claims agent immediately:</p>
                <p>Name: Dr. James Williams<br>
                Email: claims_processing@int-lottery-payments.org<br>
                Phone: +44 7700 900123</p>
                <p>You must provide the following information to claim your prize:</p>
                <ol>
                <li>Full Name</li>
                <li>Address</li>
                <li>Phone Number</li>
                <li>Country of Residence</li>
                <li>Age</li>
                <li>Occupation</li>
                <li>Winning Ticket Number: INT-7752-8921-3347</li>
                </ol>
                <p>NOTE: For security reasons, you are advised to keep your winning information confidential until your claim is processed and your money remitted to you.</p>
                <p>Congratulations once again!</p>
                <p>Sincerely,<br>
                Dr. Robert Johnson<br>
                International Lottery Commission</p>
                </body>
                </html>
                """,
                "body_text": """
                CONGRATULATIONS!!!
                
                Dear Lucky Winner,
                
                We are pleased to inform you that your email address was randomly selected as the winner of our INTERNATIONAL EMAIL LOTTERY PROGRAM held on {{DATE}}.
                
                You have been awarded the sum of FIVE MILLION UNITED STATES DOLLARS ($5,000,000.00 USD).
                
                To claim your prize, you must contact our claims agent immediately:
                
                Name: Dr. James Williams
                Email: claims_processing@int-lottery-payments.org
                Phone: +44 7700 900123
                
                You must provide the following information to claim your prize:
                1. Full Name
                2. Address
                3. Phone Number
                4. Country of Residence
                5. Age
                6. Occupation
                7. Winning Ticket Number: INT-7752-8921-3347
                
                NOTE: For security reasons, you are advised to keep your winning information confidential until your claim is processed and your money remitted to you.
                
                Congratulations once again!
                
                Sincerely,
                Dr. Robert Johnson
                International Lottery Commission
                """,
                "indicators": [
                    "ALL CAPS and excessive punctuation",
                    "Unsolicited lottery win",
                    "Requests personal information",
                    "Foreign phone number",
                    "Suspicious domain",
                    "Request for secrecy",
                    "Implausible amount of money"
                ],
                "target_platforms": ["General Public", "Elderly", "Non-technical users"]
            },
            {
                "name": "Fake Pharmacy",
                "subject": "70% OFF all meds - Limited Time Only!",
                "sender_name": "Canadian Pharmacy",
                "sender_email": "discounts@canadian-pharmacy-rxsavings.com",
                "body_html": """
                <html>
                <body>
                <h2>SPECIAL DISCOUNT OFFER</h2>
                <p>Dear Valued Customer,</p>
                <p>For a LIMITED TIME ONLY, our Canadian Pharmacy is offering a 70% DISCOUNT on all medications!</p>
                <p>✓ 100% FDA Approved Medications<br>
                ✓ No Prescription Needed<br>
                ✓ Express Shipping Worldwide<br>
                ✓ Complete Confidentiality</p>
                <p><b>Our Best Sellers:</b></p>
                <ul>
                <li>Viagra (100mg) - $1.50/pill</li>
                <li>Cialis (20mg) - $2.00/pill</li>
                <li>Levitra (20mg) - $2.50/pill</li>
                <li>Pain Medications - LOWEST PRICE GUARANTEED!</li>
                <li>Weight Loss Pills - SPECIAL DISCOUNT!</li>
                </ul>
                <p><a href="{{MALICIOUS_LINK}}">CLICK HERE TO SHOP NOW</a></p>
                <p>This offer expires in 48 hours!</p>
                <p>***To be removed from our mailing list, reply with "REMOVE" in the subject line.***</p>
                </body>
                </html>
                """,
                "body_text": """
                SPECIAL DISCOUNT OFFER
                
                Dear Valued Customer,
                
                For a LIMITED TIME ONLY, our Canadian Pharmacy is offering a 70% DISCOUNT on all medications!
                
                ✓ 100% FDA Approved Medications
                ✓ No Prescription Needed
                ✓ Express Shipping Worldwide
                ✓ Complete Confidentiality
                
                Our Best Sellers:
                * Viagra (100mg) - $1.50/pill
                * Cialis (20mg) - $2.00/pill
                * Levitra (20mg) - $2.50/pill
                * Pain Medications - LOWEST PRICE GUARANTEED!
                * Weight Loss Pills - SPECIAL DISCOUNT!
                
                CLICK HERE TO SHOP NOW: {{MALICIOUS_LINK}}
                
                This offer expires in 48 hours!
                
                ***To be removed from our mailing list, reply with "REMOVE" in the subject line.***
                """,
                "indicators": [
                    "Too-good-to-be-true pricing",
                    "ALL CAPS and excessive punctuation",
                    "Suspicious domain name",
                    "Offers prescription drugs without prescription",
                    "False urgency with time limit",
                    "Unsolicited pharmaceutical offer"
                ],
                "target_platforms": ["General Public", "Elderly", "Health-conscious individuals"]
            }
        ]
        
        # Spear phishing email templates
        self.templates["spear_phishing"] = [
            {
                "name": "CEO Wire Transfer Request",
                "subject": "Urgent wire transfer needed",
                "sender_name": "{{CEO_NAME}}",
                "sender_email": "{{CEO_NAME_LOWERCASE}}@{{COMPANY_DOMAIN_TYPO}}",
                "body_html": """
                <html>
                <body>
                <p>Hi {{FIRST_NAME}},</p>
                <p>I need you to process an urgent wire transfer for a new vendor we're working with on the {{PROJECT_NAME}} project. This is time-sensitive and needs to be completed today.</p>
                <p>Amount: ${{AMOUNT}}<br>
                Beneficiary Name: {{BENEFICIARY_NAME}}<br>
                Bank: {{BANK_NAME}}<br>
                Account Number: {{ACCOUNT_NUMBER}}<br>
                Routing Number: {{ROUTING_NUMBER}}<br>
                Reference: {{PROJECT_NAME}} initial payment</p>
                <p>Please confirm once this is complete. I'm in meetings all day but will check my email periodically.</p>
                <p>Thanks for taking care of this quickly,<br>
                {{CEO_NAME}}</p>
                <p><i>Sent from my iPhone</i></p>
                </body>
                </html>
                """,
                "body_text": """
                Hi {{FIRST_NAME}},
                
                I need you to process an urgent wire transfer for a new vendor we're working with on the {{PROJECT_NAME}} project. This is time-sensitive and needs to be completed today.
                
                Amount: ${{AMOUNT}}
                Beneficiary Name: {{BENEFICIARY_NAME}}
                Bank: {{BANK_NAME}}
                Account Number: {{ACCOUNT_NUMBER}}
                Routing Number: {{ROUTING_NUMBER}}
                Reference: {{PROJECT_NAME}} initial payment
                
                Please confirm once this is complete. I'm in meetings all day but will check my email periodically.
                
                Thanks for taking care of this quickly,
                {{CEO_NAME}}
                
                Sent from my iPhone
                """,
                "indicators": [
                    "Spoofed email with typo in domain",
                    "Urgency and time pressure",
                    "Request for wire transfer",
                    "Sender 'unavailable' for verbal confirmation",
                    "Mobile signature to explain terse communication",
                    "Exploits authority of CEO"
                ],
                "target_platforms": ["Finance Department", "Accounting", "Administrative Assistants"]
            },
            {
                "name": "HR Document Review",
                "subject": "Please review: Updated Employee Benefits 2024",
                "sender_name": "{{HR_DIRECTOR_NAME}}",
                "sender_email": "{{HR_DIRECTOR_EMAIL_USERNAME}}@{{COMPANY_DOMAIN_TYPO}}",
                "body_html": """
                <html>
                <body>
                <p>Hello {{FIRST_NAME}},</p>
                <p>I'm sharing our updated employee benefits documentation for 2024 for your review. Please take a look at these changes before our all-hands meeting next Monday.</p>
                <p>The key updates include:</p>
                <ul>
                <li>New healthcare provider options</li>
                <li>Enhanced retirement matching program</li>
                <li>Revised PTO policy</li>
                <li>Work from home policy updates</li>
                </ul>
                <p>Please review the documents here: <a href="{{MALICIOUS_LINK}}">{{COMPANY_NAME}} Benefits 2024.pdf</a></p>
                <p>You'll need to login with your company credentials to access the document. Let me know if you have any questions.</p>
                <p>Best regards,<br>
                {{HR_DIRECTOR_NAME}}<br>
                Director of Human Resources<br>
                {{COMPANY_NAME}}</p>
                </body>
                </html>
                """,
                "body_text": """
                Hello {{FIRST_NAME}},
                
                I'm sharing our updated employee benefits documentation for 2024 for your review. Please take a look at these changes before our all-hands meeting next Monday.
                
                The key updates include:
                * New healthcare provider options
                * Enhanced retirement matching program
                * Revised PTO policy
                * Work from home policy updates
                
                Please review the documents here: {{MALICIOUS_LINK}}
                
                You'll need to login with your company credentials to access the document. Let me know if you have any questions.
                
                Best regards,
                {{HR_DIRECTOR_NAME}}
                Director of Human Resources
                {{COMPANY_NAME}}
                """,
                "indicators": [
                    "Slightly misspelled domain name",
                    "Request for login credentials",
                    "Topics of interest to all employees",
                    "Impersonation of HR personnel",
                    "Well-crafted with company-specific details"
                ],
                "target_platforms": ["All Employees", "Corporate"]
            }
        ]
        
        # Business Email Compromise templates
        self.templates["business_email_compromise"] = [
            {
                "name": "Vendor Payment Change Request",
                "subject": "URGENT: Updated banking information for invoice payments",
                "sender_name": "{{VENDOR_CONTACT_NAME}}",
                "sender_email": "{{VENDOR_CONTACT_NAME_LOWERCASE}}@{{VENDOR_DOMAIN_TYPO}}",
                "body_html": """
                <html>
                <body>
                <p>Dear {{ACCOUNTS_PAYABLE_NAME}},</p>
                <p>I hope this email finds you well. I am writing to inform you that {{VENDOR_COMPANY}} has recently changed our banking details for all future invoice payments, effective immediately.</p>
                <p>Please update your records with our new banking information:</p>
                <p>Bank Name: {{BANK_NAME}}<br>
                Account Name: {{VENDOR_COMPANY}}<br>
                Account Number: {{NEW_ACCOUNT_NUMBER}}<br>
                Routing Number: {{NEW_ROUTING_NUMBER}}<br>
                Bank Address: {{BANK_ADDRESS}}</p>
                <p>We have several outstanding invoices that need to be processed with the new banking details, including invoice #{{INVOICE_NUMBER}} for ${{AMOUNT}}.</p>
                <p>Please confirm receipt of this email and that the banking details have been updated in your system.</p>
                <p>Thank you for your prompt attention to this matter.</p>
                <p>Best regards,<br>
                {{VENDOR_CONTACT_NAME}}<br>
                Accounts Receivable<br>
                {{VENDOR_COMPANY}}</p>
                </body>
                </html>
                """,
                "body_text": """
                Dear {{ACCOUNTS_PAYABLE_NAME}},
                
                I hope this email finds you well. I am writing to inform you that {{VENDOR_COMPANY}} has recently changed our banking details for all future invoice payments, effective immediately.
                
                Please update your records with our new banking information:
                
                Bank Name: {{BANK_NAME}}
                Account Name: {{VENDOR_COMPANY}}
                Account Number: {{NEW_ACCOUNT_NUMBER}}
                Routing Number: {{NEW_ROUTING_NUMBER}}
                Bank Address: {{BANK_ADDRESS}}
                
                We have several outstanding invoices that need to be processed with the new banking details, including invoice #{{INVOICE_NUMBER}} for ${{AMOUNT}}.
                
                Please confirm receipt of this email and that the banking details have been updated in your system.
                
                Thank you for your prompt attention to this matter.
                
                Best regards,
                {{VENDOR_CONTACT_NAME}}
                Accounts Receivable
                {{VENDOR_COMPANY}}
                """,
                "indicators": [
                    "Domain typo in sender email",
                    "Request to change payment information",
                    "Urgency in subject line",
                    "Reference to specific, legitimate-sounding invoices",
                    "Request for confirmation",
                    "Impersonation of known vendor contact"
                ],
                "target_platforms": ["Accounts Payable", "Finance Department", "Procurement"]
            },
            {
                "name": "Executive Assistant Request",
                "subject": "Help needed with quick task",
                "sender_name": "{{EXECUTIVE_NAME}}",
                "sender_email": "{{EXECUTIVE_EMAIL}}",
                "body_html": """
                <html>
                <body>
                <p>Hi {{ASSISTANT_NAME}},</p>
                <p>Hope you're doing well. I'm currently in a conference and need your help with a quick task.</p>
                <p>I need to send some gift cards to clients as a thank you for the {{PROJECT_NAME}} project. Could you purchase {{NUMBER_OF_CARDS}} Amazon gift cards valued at ${{GIFT_CARD_AMOUNT}} each?</p>
                <p>Please keep this confidential as it's a surprise for the team too. I'll need the gift card codes emailed to me as soon as possible.</p>
                <p>Let me know if you can help with this today.</p>
                <p>Thanks,<br>
                {{EXECUTIVE_NAME}}</p>
                <p><i>Sent from my mobile device</i></p>
                </body>
                </html>
                """,
                "body_text": """
                Hi {{ASSISTANT_NAME}},
                
                Hope you're doing well. I'm currently in a conference and need your help with a quick task.
                
                I need to send some gift cards to clients as a thank you for the {{PROJECT_NAME}} project. Could you purchase {{NUMBER_OF_CARDS}} Amazon gift cards valued at ${{GIFT_CARD_AMOUNT}} each?
                
                Please keep this confidential as it's a surprise for the team too. I'll need the gift card codes emailed to me as soon as possible.
                
                Let me know if you can help with this today.
                
                Thanks,
                {{EXECUTIVE_NAME}}
                
                Sent from my mobile device
                """,
                "indicators": [
                    "Request for gift cards (common scam)",
                    "Urgency and immediate action required",
                    "Request for secrecy",
                    "Exploits assistant's desire to help executive",
                    "Mobile signature to explain brief communication",
                    "Executed while executive is supposedly unavailable for verification"
                ],
                "target_platforms": ["Executive Assistants", "Administrative Staff"]
            }
        ]
        
        # Malware delivery templates
        self.templates["malware_delivery"] = [
            {
                "name": "Invoice Attachment",
                "subject": "Invoice #{{INVOICE_NUMBER}} for {{MONTH}} {{YEAR}}",
                "sender_name": "{{COMPANY_NAME}} Billing",
                "sender_email": "billing@{{COMPANY_DOMAIN_TYPO}}",
                "body_html": """
                <html>
                <body>
                <p>Dear Valued Customer,</p>
                <p>Please find attached your invoice #{{INVOICE_NUMBER}} for {{MONTH}} {{YEAR}} in the amount of ${{AMOUNT}}.</p>
                <p>Payment is due by {{DUE_DATE}}. Please remit payment according to the terms outlined in the invoice.</p>
                <p>If you have any questions regarding this invoice, please contact our billing department at billing@{{COMPANY_DOMAIN}} or call (800) 555-0123.</p>
                <p>Thank you for your business.</p>
                <p>Sincerely,<br>
                {{BILLING_PERSON_NAME}}<br>
                Billing Department<br>
                {{COMPANY_NAME}}</p>
                <p>ATTACHMENT: <a href="{{MALICIOUS_LINK}}">Invoice_{{INVOICE_NUMBER}}.doc</a></p>
                </body>
                </html>
                """,
                "body_text": """
                Dear Valued Customer,
                
                Please find attached your invoice #{{INVOICE_NUMBER}} for {{MONTH}} {{YEAR}} in the amount of ${{AMOUNT}}.
                
                Payment is due by {{DUE_DATE}}. Please remit payment according to the terms outlined in the invoice.
                
                If you have any questions regarding this invoice, please contact our billing department at billing@{{COMPANY_DOMAIN}} or call (800) 555-0123.
                
                Thank you for your business.
                
                Sincerely,
                {{BILLING_PERSON_NAME}}
                Billing Department
                {{COMPANY_NAME}}
                
                ATTACHMENT: Invoice_{{INVOICE_NUMBER}}.doc ({{MALICIOUS_LINK}})
                """,
                "indicators": [
                    "Typo in sender domain",
                    "Generic greeting",
                    "Suspicious file attachment (.doc format)",
                    "Malicious link disguised as document download",
                    "Financial subject to create urgency",
                    "Professional formatting to appear legitimate"
                ],
                "target_platforms": ["Accounts Payable", "Finance Department", "Small Businesses"]
            },
            {
                "name": "Shipping Confirmation",
                "subject": "Your order #{{ORDER_NUMBER}} has shipped",
                "sender_name": "{{ECOMMERCE_SITE}} Shipping",
                "sender_email": "shipping@{{ECOMMERCE_DOMAIN_TYPO}}",
                "body_html": """
                <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background-color: #f0f0f0; padding: 20px; text-align: center;">
                        <h1 style="color: #0066cc;">Your Order Has Shipped!</h1>
                    </div>
                    
                    <div style="padding: 20px;">
                        <p>Hello {{FIRST_NAME}},</p>
                        <p>Great news! Your order #{{ORDER_NUMBER}} has shipped and is on its way to you.</p>
                        <p><strong>Estimated delivery date:</strong> {{DELIVERY_DATE}}</p>
                        
                        <div style="background-color: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin: 20px 0; border-radius: 5px;">
                            <h3>Order Details:</h3>
                            <p><strong>Order #:</strong> {{ORDER_NUMBER}}<br>
                            <strong>Order Date:</strong> {{ORDER_DATE}}<br>
                            <strong>Shipping Method:</strong> {{SHIPPING_METHOD}}</p>
                        </div>
                        
                        <p>To track your package or view your order details, please click the link below:</p>
                        
                        <div style="text-align: center; margin: 25px 0;">
                            <a href="{{MALICIOUS_LINK}}" style="background-color: #0066cc; color: white; padding: 12px 35px; text-decoration: none; font-weight: bold; border-radius: 5px;">TRACK YOUR ORDER</a>
                        </div>
                        
                        <p><strong>Note:</strong> If you did not place this order or have any questions, please contact our customer service team immediately.</p>
                        
                        <p>Thank you for shopping with {{ECOMMERCE_SITE}}!</p>
                    </div>
                    
                    <div style="background-color: #0066cc; color: white; padding: 20px; text-align: center; font-size: 12px;">
                        <p>© {{YEAR}} {{ECOMMERCE_SITE}} | <a href="#" style="color: white;">Privacy Policy</a> | <a href="#" style="color: white;">Terms of Service</a></p>
                    </div>
                </body>
                </html>
                """,
                "body_text": """
                Your Order Has Shipped!
                
                Hello {{FIRST_NAME}},
                
                Great news! Your order #{{ORDER_NUMBER}} has shipped and is on its way to you.
                
                Estimated delivery date: {{DELIVERY_DATE}}
                
                Order Details:
                Order #: {{ORDER_NUMBER}}
                Order Date: {{ORDER_DATE}}
                Shipping Method: {{SHIPPING_METHOD}}
                
                To track your package or view your order details, please click the link below:
                
                TRACK YOUR ORDER: {{MALICIOUS_LINK}}
                
                Note: If you did not place this order or have any questions, please contact our customer service team immediately.
                
                Thank you for shopping with {{ECOMMERCE_SITE}}!
                
                © {{YEAR}} {{ECOMMERCE_SITE}} | Privacy Policy | Terms of Service
                """,
                "indicators": [
                    "Typo in sender domain",
                    "Professional-looking formatting",
                    "Legitimate-seeming order number",
                    "Malicious link disguised as tracking link",
                    "Exploits curiosity about package/order",
                    "May target victims who are expecting packages"
                ],
                "target_platforms": ["E-commerce Customers", "General Public"]
            }
        ]
    
    def get_template_categories(self) -> List[str]:
        """
        Get a list of available template categories
        
        Returns:
            List of template category names
        """
        return list(self.templates.keys())
    
    def get_template_count(self) -> Dict[str, int]:
        """
        Get the count of templates in each category
        
        Returns:
            Dictionary with category names as keys and counts as values
        """
        if not self.loaded:
            self.load_templates()
            
        return {category: len(templates) for category, templates in self.templates.items()}
    
    def get_templates_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all templates in a specific category
        
        Args:
            category: Category name
            
        Returns:
            List of template dictionaries
        """
        if not self.loaded:
            self.load_templates()
            
        if category not in self.templates:
            return []
            
        return self.templates[category]
    
    def get_template_by_name(self, name: str, category: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get a specific template by name
        
        Args:
            name: Template name
            category: Optional category (if known)
            
        Returns:
            Template dictionary or None if not found
        """
        if not self.loaded:
            self.load_templates()
            
        # If category is provided, search only in that category
        if category and category in self.templates:
            for template in self.templates[category]:
                if template["name"] == name:
                    return template
        else:
            # Search in all categories
            for category_templates in self.templates.values():
                for template in category_templates:
                    if template["name"] == name:
                        return template
                        
        return None
    
    def create_customized_template(self, template_name: str, category: str, variables: Dict[str, str]) -> Dict[str, Any]:
        """
        Create a customized version of a template with specific variables
        
        Args:
            template_name: Name of the template to customize
            category: Category of the template
            variables: Dictionary of variable values to insert
            
        Returns:
            Customized template dictionary
        """
        template = self.get_template_by_name(template_name, category)
        if not template:
            raise ValueError(f"Template '{template_name}' not found in category '{category}'")
            
        # Create a copy of the template
        customized = template.copy()
        
        # Replace variables in subject, body_html and body_text
        customized["subject"] = self._replace_variables(customized["subject"], variables)
        customized["body_html"] = self._replace_variables(customized["body_html"], variables)
        customized["body_text"] = self._replace_variables(customized["body_text"], variables)
        
        # Include the variables used for reference
        customized["variables_used"] = variables
        
        return customized
    
    def _replace_variables(self, text: str, variables: Dict[str, str]) -> str:
        """
        Replace template variables in text
        
        Args:
            text: Text with variables
            variables: Dictionary of variable values
            
        Returns:
            Text with variables replaced
        """
        result = text
        
        # Replace user-provided variables
        for var_name, var_value in variables.items():
            if var_name.startswith("{{") and var_name.endswith("}}"):
                var_key = var_name
            else:
                var_key = "{{" + var_name + "}}"
                
            result = result.replace(var_key, var_value)
            
        # Replace any missing variables with default values from self.variables
        for var_name, default_value in self.variables.items():
            if var_name in result:
                result = result.replace(var_name, default_value)
                
        return result
    
    def get_all_variable_names(self) -> List[str]:
        """
        Get a list of all variable names used in templates
        
        Returns:
            List of variable names
        """
        return list(self.variables.keys())
    
    def save_template(self, template: Dict[str, Any], category: str) -> bool:
        """
        Save a template to the specified category
        
        Args:
            template: Template dictionary
            category: Category to save template in
            
        Returns:
            Boolean indicating success
        """
        if not self.loaded:
            self.load_templates()
            
        if category not in self.templates:
            return False
            
        # Check if template with this name already exists
        for existing in self.templates[category]:
            if existing["name"] == template["name"]:
                # Replace existing template
                existing.update(template)
                return True
                
        # Add new template
        self.templates[category].append(template)
        
        # In a real implementation, we would save to disk:
        # try:
        #     category_path = os.path.join(self.templates_dir, category)
        #     os.makedirs(category_path, exist_ok=True)
        #     
        #     filename = os.path.join(category_path, f"{template['name'].lower().replace(' ', '_')}.json")
        #     with open(filename, 'w') as f:
        #         json.dump(template, f, indent=2)
        #     
        #     return True
        # except Exception as e:
        #     logger.error(f"Error saving template: {str(e)}")
        #     return False
        
        return True
    
    def delete_template(self, template_name: str, category: str) -> bool:
        """
        Delete a template from the specified category
        
        Args:
            template_name: Name of template to delete
            category: Category to delete from
            
        Returns:
            Boolean indicating success
        """
        if not self.loaded:
            self.load_templates()
            
        if category not in self.templates:
            return False
            
        # Find template by name
        for i, template in enumerate(self.templates[category]):
            if template["name"] == template_name:
                # Remove template
                self.templates[category].pop(i)
                
                # In a real implementation, we would delete from disk:
                # try:
                #     filename = os.path.join(self.templates_dir, category, f"{template_name.lower().replace(' ', '_')}.json")
                #     if os.path.exists(filename):
                #         os.remove(filename)
                # except Exception as e:
                #     logger.error(f"Error deleting template file: {str(e)}")
                
                return True
                
        return False
    
    def search_templates(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for templates matching a query string
        
        Args:
            query: Search query string
            
        Returns:
            List of matching template dictionaries
        """
        if not self.loaded:
            self.load_templates()
            
        results = []
        query = query.lower()
        
        for category, templates in self.templates.items():
            for template in templates:
                # Search in name, subject, and body
                if query in template["name"].lower() or \
                   query in template["subject"].lower() or \
                   query in template["body_text"].lower():
                    # Add category to the result
                    result = template.copy()
                    result["category"] = category
                    results.append(result)
                    
        return results
