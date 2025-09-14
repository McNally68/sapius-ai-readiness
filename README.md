# Sapius AI Readiness Assessment Platform

A comprehensive web application for evaluating organizational readiness for AI adoption, developed by Sapius Limited.

## Overview

The Sapius AI Readiness Assessment Platform helps organizations understand their current AI maturity level and provides personalized recommendations for successful AI implementation. The platform evaluates six critical dimensions of AI readiness through a research-based framework.

## Features

### 🎯 **Core Functionality**
- **Comprehensive Assessment**: 15-minute evaluation covering all aspects of AI readiness
- **Personalized Results**: Tailored recommendations based on assessment responses
- **Interactive Dashboard**: Real-time scoring and progress tracking
- **Detailed Reports**: Comprehensive analysis with actionable insights

### 📊 **Assessment Dimensions**
1. **Leadership & Strategy** (25% weight) - Strategic commitment and leadership alignment
2. **Organizational Culture** (20% weight) - Learning culture and change readiness
3. **Data Infrastructure** (20% weight) - Data quality and management capabilities
4. **Process Readiness** (15% weight) - Workflow documentation and integration
5. **Technical Capabilities** (10% weight) - Technology stack and AI integration readiness
6. **Skills & Talent** (10% weight) - AI literacy and technical expertise

### 🔧 **Resource Library**
- **Data Preparation Resources**: 27+ publicly available tools and guides
- **Technology Stack Resources**: 40+ platforms, frameworks, and infrastructure tools
- **Implementation Guides**: Best practices and industry insights
- **Research Papers**: Academic and industry whitepapers

## Technology Stack

### **Backend**
- **Python 3.13+**
- **Flask 3.1.3** - Web framework
- **Werkzeug** - WSGI utility library

### **Frontend**
- **Bootstrap 5.1.3** - Responsive CSS framework
- **Font Awesome 6.0** - Icon library
- **Google Fonts** - Typography (Source Sans Pro, League Spartan)
- **Custom CSS** - Sapius brand styling

### **Architecture**
- **MVC Pattern** - Clean separation of concerns
- **Session Management** - Secure result storage
- **Static File Serving** - Optimized asset delivery
- **Responsive Design** - Mobile-first approach

## Installation & Setup

### **Prerequisites**
- Python 3.13 or higher
- pip package manager

### **Installation**
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AIReady
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser to `http://127.0.0.1:5001`

### **Dependencies**
```
Flask==3.1.3
Werkzeug==3.1.3
```

## Project Structure

```
AIReady/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
├── static/                        # Static assets
│   ├── css/
│   │   └── style.css             # Custom Sapius styling
│   ├── js/
│   │   └── app.js                # Frontend JavaScript
│   └── images/
│       ├── sapius-strategy-logo.png
│       └── aiready1.jpg
└── templates/                     # HTML templates
    ├── base.html                  # Base template
    ├── index.html                 # Homepage
    ├── assessment.html            # Assessment form
    ├── results.html              # Results page
    ├── resources.html            # Resource library
    ├── data_preparation.html     # Data prep resources
    └── technology_stack.html     # Technology resources
```

## Usage Guide

### **Taking an Assessment**
1. Navigate to the homepage at `http://127.0.0.1:5001`
2. Click "Start Assessment" to begin
3. Complete the multi-section questionnaire
4. Receive instant personalized results
5. Download or share your assessment report

### **Accessing Resources**
1. Visit the Resources section from the navigation menu
2. Browse by category (Data Preparation, Technology Stack, etc.)
3. Click on resource cards to access detailed guides
4. Follow external links to official documentation and tools

### **Assessment Scoring**
- Each question is scored 1-5 points
- Category scores are weighted according to research-based importance
- Overall readiness score is calculated as a weighted average
- Recommendations are generated based on category performance

## API Endpoints

### **Web Routes**
- `GET /` - Homepage
- `GET /assessment` - Assessment form
- `GET /results/<assessment_id>` - Results page
- `GET /resources` - Resource library
- `GET /resources/data-preparation` - Data preparation resources
- `GET /resources/technology-stack` - Technology stack resources

### **API Routes**
- `POST /api/submit_assessment` - Submit assessment responses
  - **Input**: JSON with responses and company info
  - **Output**: Assessment ID, scores, and recommendations

## Customization

### **Branding**
The application uses Sapius Limited branding:
- **Logo**: Sapius Strategy logo in navigation
- **Colors**: Black/white/grayscale theme
- **Typography**: Source Sans Pro and League Spartan fonts
- **Footer**: Official Sapius company information

### **Styling**
Custom CSS variables for easy theme modification:
```css
:root {
    --primary-color: #000000;
    --secondary-color: #6b7280;
    --light-bg: #ffffff;
    --dark-bg: #000000;
    --border-radius: 0px;
}
```

## Development

### **Running in Development Mode**
```bash
python app.py
```
- Debug mode enabled
- Auto-reload on file changes
- Detailed error messages

### **Adding New Resources**
1. Create new route in `app.py`
2. Add corresponding HTML template
3. Update navigation links
4. Follow existing styling patterns

## Deployment

### **Production Considerations**
- Use production WSGI server (Gunicorn, uWSGI)
- Configure environment variables
- Set up proper logging
- Implement security headers
- Use HTTPS in production

### **Environment Variables**
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

## Legal & Compliance

### **Company Information**
- **Company**: Sapius Limited
- **Registration**: England and Wales
- **Company Number**: 15572793
- **Address**: The Old Bank, 4 Bank Terrace, Gomshall Lane, Shere, Surrey, UK, GU5 9HB

### **Privacy**
- Privacy Policy: https://sapius.co.uk/privacy-policy
- Assessment data stored in session only
- No persistent user data collection

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes following existing patterns
4. Test thoroughly
5. Submit pull request

## Support

For technical support or questions about AI readiness assessment:
- Visit: https://sapius.co.uk
- Email: Contact through Sapius website

## License

© 2024 Sapius Limited. All rights reserved.

---

**Built with insights from organizational AI research to help companies successfully navigate their AI transformation journey.**