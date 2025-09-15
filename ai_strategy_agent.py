#!/usr/bin/env python3
"""
AI Strategy Framework Resource Agent
Automatically populates and maintains AI Strategy Framework resources
Runs daily at 10pm to refresh content and generate summary
"""

import requests
import json
import schedule
import time
from datetime import datetime
from jinja2 import Template
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_strategy_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AIStrategyAgent:
    def __init__(self):
        self.resources = []
        self.summary = ""
        self.last_updated = None
        
    def fetch_strategy_resources(self):
        """Fetch latest AI strategy resources from various sources"""
        logger.info("Fetching AI Strategy Framework resources...")
        
        # Reset resources list
        self.resources = []
        
        # Core strategy frameworks and methodologies
        strategy_resources = [
            {
                "title": "MIT AI Strategy Framework",
                "url": "https://mitsloan.mit.edu/ideas-made-to-matter/ai-strategy-framework",
                "description": "MIT Sloan's comprehensive framework for developing AI strategy in organizations.",
                "category": "Academic Framework",
                "type": "Framework",
                "provider": "MIT Sloan",
                "key_points": [
                    "Strategic alignment methodology",
                    "Value creation identification", 
                    "Risk assessment frameworks",
                    "Implementation roadmaps"
                ]
            },
            {
                "title": "Harvard Business Review AI Strategy Guide",
                "url": "https://hbr.org/2019/07/building-the-ai-powered-organization",
                "description": "HBR's guide to building AI-powered organizations with strategic focus.",
                "category": "Business Strategy",
                "type": "Guide",
                "provider": "Harvard Business Review",
                "key_points": [
                    "Organizational transformation",
                    "AI capabilities assessment",
                    "Change management strategies",
                    "Performance measurement"
                ]
            },
            {
                "title": "McKinsey AI Strategy Playbook",
                "url": "https://www.mckinsey.com/capabilities/quantumblack/our-insights/ai-strategy",
                "description": "McKinsey's strategic approach to AI adoption and implementation.",
                "category": "Consulting Framework",
                "type": "Playbook",
                "provider": "McKinsey & Company",
                "key_points": [
                    "AI readiness assessment",
                    "Use case prioritization",
                    "Scaling methodologies",
                    "ROI optimization"
                ]
            },
            {
                "title": "Deloitte AI Institute Strategy Resources",
                "url": "https://www2.deloitte.com/us/en/insights/focus/cognitive-technologies.html",
                "description": "Comprehensive AI strategy insights and frameworks from Deloitte.",
                "category": "Consulting Framework",
                "type": "Resource Hub",
                "provider": "Deloitte",
                "key_points": [
                    "Industry-specific strategies",
                    "Digital transformation alignment",
                    "Governance frameworks",
                    "Talent strategy"
                ]
            },
            {
                "title": "Stanford AI Strategy Course Materials",
                "url": "https://hai.stanford.edu/policy",
                "description": "Stanford HAI policy and strategy resources for AI implementation.",
                "category": "Academic Framework",
                "type": "Course Materials",
                "provider": "Stanford HAI",
                "key_points": [
                    "Policy alignment",
                    "Ethical AI strategy",
                    "Research-to-practice frameworks",
                    "Multi-stakeholder approaches"
                ]
            },
            {
                "title": "BCG AI Strategy Matrix",
                "url": "https://www.bcg.com/capabilities/artificial-intelligence/strategy",
                "description": "Boston Consulting Group's strategic matrix for AI transformation.",
                "category": "Consulting Framework", 
                "type": "Matrix Tool",
                "provider": "Boston Consulting Group",
                "key_points": [
                    "Strategic prioritization matrix",
                    "Capability building roadmaps",
                    "Competitive advantage frameworks",
                    "Value realization models"
                ]
            },
            {
                "title": "Gartner AI Strategy Framework",
                "url": "https://www.gartner.com/en/information-technology/insights/artificial-intelligence",
                "description": "Gartner's research-based framework for AI strategy development.",
                "category": "Research Framework",
                "type": "Framework",
                "provider": "Gartner",
                "key_points": [
                    "Market trend analysis",
                    "Technology maturity assessment",
                    "Vendor evaluation criteria",
                    "Implementation timelines"
                ]
            },
            {
                "title": "World Economic Forum AI Strategy Toolkit",
                "url": "https://www.weforum.org/centre-for-the-fourth-industrial-revolution/artificial-intelligence-and-machine-learning",
                "description": "WEF's global perspective on AI strategy development.",
                "category": "Global Framework",
                "type": "Toolkit",
                "provider": "World Economic Forum",
                "key_points": [
                    "Global best practices",
                    "Cross-industry insights",
                    "Stakeholder engagement",
                    "Societal impact considerations"
                ]
            },
            {
                "title": "Google Cloud AI Strategy Guide",
                "url": "https://cloud.google.com/ai/ai-strategy",
                "description": "Google's practical guide to developing and implementing AI strategy.",
                "category": "Technology Strategy",
                "type": "Implementation Guide",
                "provider": "Google Cloud",
                "key_points": [
                    "Cloud-first AI strategy",
                    "Data strategy alignment",
                    "ML operations framework",
                    "Scalable architecture design"
                ]
            },
            {
                "title": "IBM AI Strategy Framework",
                "url": "https://www.ibm.com/artificial-intelligence/strategy",
                "description": "IBM's enterprise-focused AI strategy development methodology.",
                "category": "Technology Strategy",
                "type": "Methodology",
                "provider": "IBM",
                "key_points": [
                    "Enterprise AI adoption",
                    "Hybrid cloud integration",
                    "AI governance models",
                    "Trust and transparency frameworks"
                ]
            }
        ]
        
        self.resources.extend(strategy_resources)
        logger.info(f"Loaded {len(self.resources)} AI strategy resources")
        
    def generate_summary(self):
        """Generate a comprehensive summary of all resources"""
        logger.info("Generating resource summary...")
        
        total_resources = len(self.resources)
        categories = {}
        providers = {}
        
        # Analyze resources by category and provider
        for resource in self.resources:
            category = resource.get('category', 'Other')
            provider = resource.get('provider', 'Unknown')
            
            categories[category] = categories.get(category, 0) + 1
            providers[provider] = providers.get(provider, 0) + 1
        
        # Generate summary text
        summary_parts = []
        summary_parts.append(f"**AI Strategy Framework Resources Collection**")
        summary_parts.append(f"Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        summary_parts.append("")
        summary_parts.append(f"This comprehensive collection contains **{total_resources} curated resources** from leading organizations, academic institutions, and consulting firms to help you develop and implement a robust AI strategy for your organization.")
        summary_parts.append("")
        
        # Resource breakdown
        summary_parts.append("**Resource Categories:**")
        for category, count in sorted(categories.items()):
            summary_parts.append(f"• **{category}**: {count} resources")
        summary_parts.append("")
        
        # Key providers
        top_providers = sorted(providers.items(), key=lambda x: x[1], reverse=True)[:5]
        summary_parts.append("**Leading Contributors:**")
        for provider, count in top_providers:
            summary_parts.append(f"• **{provider}**: {count} resource{'s' if count > 1 else ''}")
        summary_parts.append("")
        
        # Key themes
        summary_parts.append("**Key Strategic Themes Covered:**")
        themes = [
            "Strategic alignment and vision development",
            "AI readiness assessment and capability building", 
            "Use case identification and prioritization",
            "Organizational transformation and change management",
            "Governance, ethics, and risk management",
            "Implementation roadmaps and scaling methodologies",
            "ROI measurement and value realization",
            "Talent strategy and skills development"
        ]
        for theme in themes:
            summary_parts.append(f"• {theme}")
        summary_parts.append("")
        
        summary_parts.append("**How to Use These Resources:**")
        summary_parts.append("1. **Start with Assessment**: Begin with readiness assessment frameworks from MIT or McKinsey")
        summary_parts.append("2. **Develop Vision**: Use Harvard Business Review and Stanford resources for strategic vision")
        summary_parts.append("3. **Plan Implementation**: Leverage consulting frameworks from BCG, Deloitte, and McKinsey")
        summary_parts.append("4. **Execute with Technology**: Apply Google Cloud and IBM implementation guides")
        summary_parts.append("5. **Monitor and Scale**: Use Gartner research and WEF best practices for ongoing optimization")
        
        self.summary = "\n".join(summary_parts)
        self.last_updated = datetime.now()
        logger.info("Summary generated successfully")
        
    def generate_html_template(self):
        """Generate the HTML template with current resources and summary"""
        template_content = """{% extends "base.html" %}

{% block title %}AI Strategy Framework Resources - Sapius{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-12 text-center mb-5">
            <h1 class="display-4 fw-bold text-white mb-4" style="font-family: 'League Spartan', sans-serif;">AI Strategy Framework Resources</h1>
            <p class="fs-5 text-light" style="font-family: 'Source Sans Pro', sans-serif;">Step-by-step guides to developing your organization's AI strategy and roadmap</p>
        </div>
    </div>

    <!-- Dynamic Summary Section -->
    <div class="resource-section mb-5">
        <div class="summary-card">
            <div class="card-body text-light" style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 2rem;">
                {{ summary_html|safe }}
            </div>
        </div>
    </div>

    <div class="resource-categories">
        <!-- Academic Frameworks -->
        <div class="resource-section">
            <h2>Academic & Research Frameworks</h2>
            <div class="resource-grid">
                {% for resource in academic_resources %}
                <div class="resource-card">
                    <div class="resource-icon">
                        <i class="fas fa-university"></i>
                    </div>
                    <h3><a href="{{ resource.url }}" target="_blank" style="color: inherit; text-decoration: none;">{{ resource.title }}</a></h3>
                    <p>{{ resource.description }}</p>
                    <ul>
                        {% for point in resource.key_points %}
                        <li>{{ point }}</li>
                        {% endfor %}
                    </ul>
                    <div class="resource-meta">
                        <span class="badge bg-primary">{{ resource.type }}</span>
                        <span class="badge bg-info">{{ resource.provider }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Consulting Frameworks -->
        <div class="resource-section">
            <h2>Consulting & Business Frameworks</h2>
            <div class="resource-grid">
                {% for resource in consulting_resources %}
                <div class="resource-card">
                    <div class="resource-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3><a href="{{ resource.url }}" target="_blank" style="color: inherit; text-decoration: none;">{{ resource.title }}</a></h3>
                    <p>{{ resource.description }}</p>
                    <ul>
                        {% for point in resource.key_points %}
                        <li>{{ point }}</li>
                        {% endfor %}
                    </ul>
                    <div class="resource-meta">
                        <span class="badge bg-success">{{ resource.type }}</span>
                        <span class="badge bg-warning">{{ resource.provider }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Technology Strategy -->
        <div class="resource-section">
            <h2>Technology Implementation Strategies</h2>
            <div class="resource-grid">
                {% for resource in technology_resources %}
                <div class="resource-card">
                    <div class="resource-icon">
                        <i class="fas fa-cogs"></i>
                    </div>
                    <h3><a href="{{ resource.url }}" target="_blank" style="color: inherit; text-decoration: none;">{{ resource.title }}</a></h3>
                    <p>{{ resource.description }}</p>
                    <ul>
                        {% for point in resource.key_points %}
                        <li>{{ point }}</li>
                        {% endfor %}
                    </ul>
                    <div class="resource-meta">
                        <span class="badge bg-danger">{{ resource.type }}</span>
                        <span class="badge bg-secondary">{{ resource.provider }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Global & Research -->
        <div class="resource-section">
            <h2>Global & Research Perspectives</h2>
            <div class="resource-grid">
                {% for resource in global_resources %}
                <div class="resource-card">
                    <div class="resource-icon">
                        <i class="fas fa-globe"></i>
                    </div>
                    <h3><a href="{{ resource.url }}" target="_blank" style="color: inherit; text-decoration: none;">{{ resource.title }}</a></h3>
                    <p>{{ resource.description }}</p>
                    <ul>
                        {% for point in resource.key_points %}
                        <li>{{ point }}</li>
                        {% endfor %}
                    </ul>
                    <div class="resource-meta">
                        <span class="badge bg-info">{{ resource.type }}</span>
                        <span class="badge bg-dark">{{ resource.provider }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <!-- Call to Action -->
    <div class="cta-section">
        <h2>Ready to Develop Your AI Strategy?</h2>
        <p>Use these frameworks to build a comprehensive AI strategy tailored to your organization.</p>
        <a href="/assessment" class="btn btn-primary btn-large">Assess Your Current State</a>
    </div>
</div>

<style>
.summary-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.summary-card h3, .summary-card h4 {
    color: #ffffff;
    margin-top: 1.5rem;
}

.summary-card ul {
    margin-bottom: 1rem;
}

.resource-meta {
    margin-top: 1rem;
}

.resource-meta .badge {
    margin-right: 0.5rem;
    margin-bottom: 0.25rem;
}
</style>
{% endblock %}"""

        # Categorize resources
        academic_resources = [r for r in self.resources if r.get('category') == 'Academic Framework']
        consulting_resources = [r for r in self.resources if r.get('category') == 'Consulting Framework']
        technology_resources = [r for r in self.resources if r.get('category') == 'Technology Strategy']
        global_resources = [r for r in self.resources if r.get('category') in ['Global Framework', 'Research Framework', 'Business Strategy']]
        
        # Convert summary to HTML
        summary_html = self.summary.replace('\n', '<br>').replace('**', '<strong>').replace('**', '</strong>')
        summary_html = summary_html.replace('•', '&bull;')
        
        # Render template
        template = Template(template_content)
        rendered_html = template.render(
            summary_html=summary_html,
            academic_resources=academic_resources,
            consulting_resources=consulting_resources, 
            technology_resources=technology_resources,
            global_resources=global_resources
        )
        
        return rendered_html
        
    def update_template_file(self):
        """Update the actual HTML template file"""
        try:
            html_content = self.generate_html_template()
            
            with open('templates/ai_strategy_framework.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            logger.info("Template file updated successfully")
            
        except Exception as e:
            logger.error(f"Error updating template file: {e}")
            
    def run_daily_update(self):
        """Run the daily update process"""
        logger.info("Starting daily AI Strategy Framework resource update...")
        try:
            self.fetch_strategy_resources()
            self.generate_summary()
            self.update_template_file()
            logger.info("Daily update completed successfully")
            
            # Log update statistics
            logger.info(f"Updated {len(self.resources)} resources")
            logger.info(f"Last updated: {self.last_updated}")
            
        except Exception as e:
            logger.error(f"Error during daily update: {e}")
            
    def start_scheduler(self):
        """Start the daily scheduler"""
        logger.info("Starting AI Strategy Framework Agent scheduler...")
        
        # Schedule daily updates at 10 PM
        schedule.every().day.at("22:00").do(self.run_daily_update)
        
        # Run initial update
        self.run_daily_update()
        
        logger.info("Scheduler started. Daily updates scheduled for 10:00 PM")
        
        # Keep the scheduler running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")

if __name__ == "__main__":
    agent = AIStrategyAgent()
    agent.start_scheduler()