import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from typing import Dict, List, Optional, Tuple
import random
import textwrap

class VisualContentGenerator:
    """Generate visual content for LinkedIn posts"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.color_schemes = self._load_color_schemes()
        self.fonts = self._get_available_fonts()
    
    def _load_templates(self) -> Dict:
        """Load visual content templates"""
        return {
            "quote_card": {
                "size": (1080, 1080),
                "layout": "centered",
                "elements": ["quote", "author", "background", "logo"]
            },
            "tip_card": {
                "size": (1080, 1350),
                "layout": "vertical",
                "elements": ["title", "tips", "background", "branding"]
            },
            "statistic_card": {
                "size": (1080, 1080),
                "layout": "split",
                "elements": ["statistic", "context", "source", "visual"]
            },
            "announcement": {
                "size": (1200, 630),
                "layout": "horizontal",
                "elements": ["headline", "details", "cta", "branding"]
            },
            "infographic": {
                "size": (1080, 1350),
                "layout": "vertical_flow",
                "elements": ["header", "data_points", "footer", "icons"]
            }
        }
    
    def _load_color_schemes(self) -> Dict:
        """Professional color schemes for LinkedIn"""
        return {
            "professional_blue": {
                "primary": "#0077B5",
                "secondary": "#00A0DC", 
                "accent": "#F3F6F8",
                "text": "#000000",
                "background": "#FFFFFF"
            },
            "corporate_gray": {
                "primary": "#2E3440",
                "secondary": "#4C566A",
                "accent": "#D8DEE9",
                "text": "#2E3440",
                "background": "#ECEFF4"
            },
            "modern_green": {
                "primary": "#2ECC71",
                "secondary": "#27AE60",
                "accent": "#E8F8F5",
                "text": "#2C3E50",
                "background": "#FFFFFF"
            },
            "elegant_purple": {
                "primary": "#8E44AD",
                "secondary": "#9B59B6",
                "accent": "#F4ECF7",
                "text": "#2C3E50",
                "background": "#FFFFFF"
            },
            "warm_orange": {
                "primary": "#E67E22",
                "secondary": "#F39C12",
                "accent": "#FEF9E7",
                "text": "#2C3E50",
                "background": "#FFFFFF"
            }
        }
    
    def _get_available_fonts(self) -> List[str]:
        """Get list of available fonts"""
        # In production, this would check system fonts
        return ["Arial", "Helvetica", "Times New Roman", "Calibri", "Georgia"]
    
    def create_quote_card(self, quote: str, author: str, 
                         color_scheme: str = "professional_blue",
                         template_style: str = "modern") -> Image.Image:
        """Create a professional quote card"""
        
        template = self.templates["quote_card"]
        colors = self.color_schemes[color_scheme]
        
        # Create image
        img = Image.new('RGB', template["size"], colors["background"])
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts (fallback to default if not available)
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            quote_font = ImageFont.truetype("arial.ttf", 36)
            author_font = ImageFont.truetype("arial.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            quote_font = ImageFont.load_default()
            author_font = ImageFont.load_default()
        
        # Add background elements
        if template_style == "modern":
            # Add subtle geometric shapes
            draw.rectangle([0, 0, 200, template["size"][1]], fill=colors["accent"])
            draw.ellipse([800, -100, 1200, 300], fill=colors["secondary"], outline=None)
        
        # Wrap and center quote text
        wrapped_quote = textwrap.fill(f'"{quote}"', width=40)
        
        # Calculate text positioning
        img_width, img_height = template["size"]
        
        # Draw quote
        quote_bbox = draw.textbbox((0, 0), wrapped_quote, font=quote_font)
        quote_width = quote_bbox[2] - quote_bbox[0]
        quote_height = quote_bbox[3] - quote_bbox[1]
        
        quote_x = (img_width - quote_width) // 2
        quote_y = (img_height - quote_height) // 2 - 50
        
        draw.multiline_text((quote_x, quote_y), wrapped_quote, 
                           fill=colors["text"], font=quote_font, align="center")
        
        # Draw author
        author_text = f"— {author}"
        author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
        author_width = author_bbox[2] - author_bbox[0]
        
        author_x = (img_width - author_width) // 2
        author_y = quote_y + quote_height + 40
        
        draw.text((author_x, author_y), author_text, 
                 fill=colors["secondary"], font=author_font)
        
        # Add branding
        brand_text = "ContentCraft AI"
        brand_x = 50
        brand_y = img_height - 80
        draw.text((brand_x, brand_y), brand_text, 
                 fill=colors["primary"], font=author_font)
        
        return img
    
    def create_tip_card(self, title: str, tips: List[str], 
                       color_scheme: str = "modern_green") -> Image.Image:
        """Create a tips/best practices card"""
        
        template = self.templates["tip_card"]
        colors = self.color_schemes[color_scheme]
        
        img = Image.new('RGB', template["size"], colors["background"])
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("arial.ttf", 42)
            tip_font = ImageFont.truetype("arial.ttf", 28)
            number_font = ImageFont.truetype("arial.ttf", 32)
        except:
            title_font = ImageFont.load_default()
            tip_font = ImageFont.load_default()
            number_font = ImageFont.load_default()
        
        img_width, img_height = template["size"]
        
        # Add header background
        draw.rectangle([0, 0, img_width, 150], fill=colors["primary"])
        
        # Draw title
        title_wrapped = textwrap.fill(title, width=30)
        draw.multiline_text((50, 40), title_wrapped, 
                           fill=colors["background"], font=title_font, align="left")
        
        # Draw tips
        y_position = 200
        for i, tip in enumerate(tips[:5], 1):  # Max 5 tips
            # Draw number circle
            circle_x, circle_y = 50, y_position
            draw.ellipse([circle_x, circle_y, circle_x + 50, circle_y + 50], 
                        fill=colors["secondary"])
            
            # Draw number
            number_bbox = draw.textbbox((0, 0), str(i), font=number_font)
            number_width = number_bbox[2] - number_bbox[0]
            number_x = circle_x + (50 - number_width) // 2
            number_y = circle_y + 8
            
            draw.text((number_x, number_y), str(i), 
                     fill=colors["background"], font=number_font)
            
            # Draw tip text
            tip_wrapped = textwrap.fill(tip, width=35)
            draw.multiline_text((120, y_position + 5), tip_wrapped, 
                               fill=colors["text"], font=tip_font)
            
            y_position += 120
        
        # Add footer branding
        draw.rectangle([0, img_height - 80, img_width, img_height], 
                      fill=colors["accent"])
        draw.text((50, img_height - 60), "ContentCraft AI - LinkedIn Tips", 
                 fill=colors["primary"], font=tip_font)
        
        return img
    
    def create_statistic_card(self, statistic: str, context: str, 
                             source: str = "", 
                             color_scheme: str = "corporate_gray") -> Image.Image:
        """Create a statistic/data visualization card"""
        
        template = self.templates["statistic_card"]
        colors = self.color_schemes[color_scheme]
        
        img = Image.new('RGB', template["size"], colors["background"])
        draw = ImageDraw.Draw(img)
        
        try:
            stat_font = ImageFont.truetype("arial.ttf", 72)
            context_font = ImageFont.truetype("arial.ttf", 32)
            source_font = ImageFont.truetype("arial.ttf", 20)
        except:
            stat_font = ImageFont.load_default()
            context_font = ImageFont.load_default()
            source_font = ImageFont.load_default()
        
        img_width, img_height = template["size"]
        
        # Add background design
        draw.rectangle([0, 0, img_width // 2, img_height], fill=colors["primary"])
        
        # Draw statistic (large number)
        stat_bbox = draw.textbbox((0, 0), statistic, font=stat_font)
        stat_width = stat_bbox[2] - stat_bbox[0]
        stat_height = stat_bbox[3] - stat_bbox[1]
        
        stat_x = (img_width // 2 - stat_width) // 2
        stat_y = (img_height - stat_height) // 2
        
        draw.text((stat_x, stat_y), statistic, 
                 fill=colors["background"], font=stat_font)
        
        # Draw context
        context_wrapped = textwrap.fill(context, width=25)
        context_x = img_width // 2 + 50
        context_y = img_height // 2 - 100
        
        draw.multiline_text((context_x, context_y), context_wrapped, 
                           fill=colors["text"], font=context_font, align="left")
        
        # Draw source
        if source:
            source_y = img_height - 100
            draw.text((context_x, source_y), f"Source: {source}", 
                     fill=colors["secondary"], font=source_font)
        
        return img
    
    def create_announcement_card(self, headline: str, details: str, 
                               cta: str = "", 
                               color_scheme: str = "warm_orange") -> Image.Image:
        """Create an announcement/news card"""
        
        template = self.templates["announcement"]
        colors = self.color_schemes[color_scheme]
        
        img = Image.new('RGB', template["size"], colors["background"])
        draw = ImageDraw.Draw(img)
        
        try:
            headline_font = ImageFont.truetype("arial.ttf", 48)
            details_font = ImageFont.truetype("arial.ttf", 28)
            cta_font = ImageFont.truetype("arial.ttf", 24)
        except:
            headline_font = ImageFont.load_default()
            details_font = ImageFont.load_default()
            cta_font = ImageFont.load_default()
        
        img_width, img_height = template["size"]
        
        # Add header stripe
        draw.rectangle([0, 0, img_width, 100], fill=colors["primary"])
        
        # Draw headline
        headline_wrapped = textwrap.fill(headline, width=40)
        draw.multiline_text((50, 20), headline_wrapped, 
                           fill=colors["background"], font=headline_font)
        
        # Draw details
        details_wrapped = textwrap.fill(details, width=60)
        draw.multiline_text((50, 150), details_wrapped, 
                           fill=colors["text"], font=details_font)
        
        # Draw CTA if provided
        if cta:
            cta_y = img_height - 100
            draw.rectangle([50, cta_y - 10, 300, cta_y + 40], 
                          fill=colors["secondary"])
            draw.text((70, cta_y), cta, fill=colors["background"], font=cta_font)
        
        return img
    
    def image_to_base64(self, img: Image.Image) -> str:
        """Convert PIL Image to base64 string for display"""
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def get_template_suggestions(self, content_type: str, topic: str) -> List[Dict]:
        """Get template suggestions based on content type and topic"""
        
        suggestions = {
            "Thought Leadership": [
                {"template": "quote_card", "reason": "Perfect for sharing insights and wisdom"},
                {"template": "statistic_card", "reason": "Great for data-driven thought leadership"}
            ],
            "Career Advice": [
                {"template": "tip_card", "reason": "Ideal for actionable career tips"},
                {"template": "quote_card", "reason": "Good for inspirational career quotes"}
            ],
            "Company News": [
                {"template": "announcement", "reason": "Perfect for company updates and news"},
                {"template": "infographic", "reason": "Great for detailed information"}
            ],
            "Professional Update": [
                {"template": "announcement", "reason": "Suitable for personal/professional updates"},
                {"template": "quote_card", "reason": "Good for sharing key learnings"}
            ]
        }
        
        return suggestions.get(content_type, [
            {"template": "quote_card", "reason": "Versatile template for any content"},
            {"template": "tip_card", "reason": "Good for educational content"}
        ])
    
    def generate_hashtag_suggestions(self, visual_type: str, topic: str) -> List[str]:
        """Generate relevant hashtags for visual content"""
        
        base_hashtags = ["#LinkedIn", "#Professional", "#ContentMarketing"]
        
        visual_hashtags = {
            "quote_card": ["#Inspiration", "#Motivation", "#Leadership", "#Wisdom"],
            "tip_card": ["#Tips", "#BestPractices", "#ProfessionalDevelopment", "#CareerAdvice"],
            "statistic_card": ["#Data", "#Statistics", "#Research", "#Insights"],
            "announcement": ["#News", "#Update", "#Announcement", "#Business"],
            "infographic": ["#Infographic", "#DataVisualization", "#Information", "#Education"]
        }
        
        topic_hashtags = {
            "Leadership": ["#Leadership", "#Management", "#ExecutiveCoaching"],
            "Technology": ["#Technology", "#Innovation", "#DigitalTransformation"],
            "Career Growth": ["#CareerGrowth", "#ProfessionalDevelopment", "#Success"],
            "Entrepreneurship": ["#Entrepreneurship", "#Startup", "#Business"]
        }
        
        suggested = base_hashtags.copy()
        suggested.extend(visual_hashtags.get(visual_type, []))
        suggested.extend(topic_hashtags.get(topic, []))
        
        return list(set(suggested))[:8]  # Return unique hashtags, max 8
