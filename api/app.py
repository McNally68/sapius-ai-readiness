#!/usr/bin/env python3
"""
AI Readiness Assessment Platform
A comprehensive tool for companies to evaluate their AI adoption readiness
Based on insights from organizational AI research
"""

from flask import Flask, render_template, request, jsonify, session, redirect
import json
import uuid
import os
from datetime import datetime

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.secret_key = 'ai_readiness_assessment_2025'

# Assessment categories and scoring weights
ASSESSMENT_CATEGORIES = {
    'leadership': {
        'name': 'Leadership & Strategy',
        'weight': 0.25,
        'description': 'Strategic commitment and leadership alignment with AI initiatives'
    },
    'culture': {
        'name': 'Organizational Culture',
        'weight': 0.20,
        'description': 'Learning culture, experimentation mindset, and change readiness'
    },
    'data': {
        'name': 'Data Infrastructure',
        'weight': 0.20,
        'description': 'Data quality, accessibility, and management capabilities'
    },
    'processes': {
        'name': 'Process Readiness',
        'weight': 0.15,
        'description': 'Workflow documentation and integration capabilities'
    },
    'technology': {
        'name': 'Technical Capabilities',
        'weight': 0.10,
        'description': 'Existing technology stack and AI integration readiness'
    },
    'skills': {
        'name': 'Skills & Talent',
        'weight': 0.10,
        'description': 'AI literacy and technical expertise in the organization'
    }
}

# Assessment questions for each category
ASSESSMENT_QUESTIONS = {
    'leadership': [
        {
            'id': 'l1',
            'question': 'How committed is senior leadership to AI adoption?',
            'options': [
                {'value': 1, 'text': 'No clear commitment or understanding'},
                {'value': 2, 'text': 'Some interest but no concrete plans'},
                {'value': 3, 'text': 'Moderate commitment with basic AI strategy'},
                {'value': 4, 'text': 'Strong commitment with well-defined AI roadmap'},
                {'value': 5, 'text': 'AI is central to organizational strategy with full C-suite buy-in'}
            ]
        },
        {
            'id': 'l2',
            'question': 'How does your organization view AI pilot failures?',
            'options': [
                {'value': 1, 'text': 'As major setbacks that discourage further investment'},
                {'value': 2, 'text': 'As concerning issues requiring blame assignment'},
                {'value': 3, 'text': 'As normal but disappointing outcomes'},
                {'value': 4, 'text': 'As valuable learning experiences'},
                {'value': 5, 'text': 'As essential stepping stones in our AI journey'}
            ]
        },
        {
            'id': 'l3',
            'question': 'How integrated is AI into your strategic decision-making?',
            'options': [
                {'value': 1, 'text': 'AI is not considered in strategic decisions'},
                {'value': 2, 'text': 'AI is occasionally mentioned but not prioritized'},
                {'value': 3, 'text': 'AI is considered for some strategic initiatives'},
                {'value': 4, 'text': 'AI potential is regularly evaluated for major decisions'},
                {'value': 5, 'text': 'AI transformation is core to all strategic planning'}
            ]
        }
    ],
    'culture': [
        {
            'id': 'c1',
            'question': 'How does your organization approach learning from AI experiments?',
            'options': [
                {'value': 1, 'text': 'We avoid experiments due to risk of failure'},
                {'value': 2, 'text': 'Limited experimentation with focus on avoiding mistakes'},
                {'value': 3, 'text': 'Some experimentation but lessons are not systematically captured'},
                {'value': 4, 'text': 'Regular experimentation with structured learning processes'},
                {'value': 5, 'text': 'Culture of rapid experimentation and contextual learning'}
            ]
        },
        {
            'id': 'c2',
            'question': 'How engaged are your teams with AI initiatives?',
            'options': [
                {'value': 1, 'text': 'Teams are resistant or disengaged'},
                {'value': 2, 'text': 'Limited engagement, mostly from IT department'},
                {'value': 3, 'text': 'Moderate interest across some business units'},
                {'value': 4, 'text': 'Good engagement with active participation'},
                {'value': 5, 'text': 'High enthusiasm and cross-functional collaboration'}
            ]
        },
        {
            'id': 'c3',
            'question': 'How does your organization manage risk in AI adoption?',
            'options': [
                {'value': 1, 'text': 'Very conservative - avoids any AI-related risks'},
                {'value': 2, 'text': 'Risk-averse with extensive approval processes'},
                {'value': 3, 'text': 'Balanced approach with standard risk management'},
                {'value': 4, 'text': 'Calculated risk-taking with proper governance'},
                {'value': 5, 'text': 'Intelligent risk-taking with rapid iteration cycles'}
            ]
        }
    ],
    'data': [
        {
            'id': 'd1',
            'question': 'How accessible is your organizational data?',
            'options': [
                {'value': 1, 'text': 'Data is heavily siloed and difficult to access'},
                {'value': 2, 'text': 'Some data silos with limited integration'},
                {'value': 3, 'text': 'Moderate data accessibility with some integration'},
                {'value': 4, 'text': 'Good data accessibility across most systems'},
                {'value': 5, 'text': 'Unified data architecture with easy access'}
            ]
        },
        {
            'id': 'd2',
            'question': 'What is the quality of your data for AI applications?',
            'options': [
                {'value': 1, 'text': 'Poor quality - unstructured and inconsistent'},
                {'value': 2, 'text': 'Below average - requires significant cleanup'},
                {'value': 3, 'text': 'Average quality - some cleaning needed'},
                {'value': 4, 'text': 'Good quality - mostly ready for AI use'},
                {'value': 5, 'text': 'High quality - AI-ready with proper governance'}
            ]
        },
        {
            'id': 'd3',
            'question': 'How well is your data governance established?',
            'options': [
                {'value': 1, 'text': 'No formal data governance processes'},
                {'value': 2, 'text': 'Basic data policies with limited enforcement'},
                {'value': 3, 'text': 'Standard data governance practices'},
                {'value': 4, 'text': 'Robust governance with clear data ownership'},
                {'value': 5, 'text': 'Comprehensive governance enabling AI innovation'}
            ]
        }
    ],
    'processes': [
        {
            'id': 'p1',
            'question': 'How well documented are your business workflows?',
            'options': [
                {'value': 1, 'text': 'Poorly documented - mostly tribal knowledge'},
                {'value': 2, 'text': 'Basic documentation with many gaps'},
                {'value': 3, 'text': 'Adequate documentation for key processes'},
                {'value': 4, 'text': 'Well documented with regular updates'},
                {'value': 5, 'text': 'Comprehensive process documentation optimized for AI integration'}
            ]
        },
        {
            'id': 'p2',
            'question': 'How adaptable are your current workflows to AI integration?',
            'options': [
                {'value': 1, 'text': 'Rigid processes that resist change'},
                {'value': 2, 'text': 'Some flexibility but significant barriers'},
                {'value': 3, 'text': 'Moderately adaptable with some redesign needed'},
                {'value': 4, 'text': 'Flexible processes ready for AI enhancement'},
                {'value': 5, 'text': 'Workflows designed with AI integration in mind'}
            ]
        }
    ],
    'technology': [
        {
            'id': 't1',
            'question': 'How modern is your technology infrastructure?',
            'options': [
                {'value': 1, 'text': 'Legacy systems with limited integration capabilities'},
                {'value': 2, 'text': 'Mostly legacy with some modern components'},
                {'value': 3, 'text': 'Mixed environment with integration challenges'},
                {'value': 4, 'text': 'Modern infrastructure with good API capabilities'},
                {'value': 5, 'text': 'Cloud-native, AI-ready architecture'}
            ]
        },
        {
            'id': 't2',
            'question': 'What is your organization\'s experience with AI/ML tools?',
            'options': [
                {'value': 1, 'text': 'No experience with AI/ML tools'},
                {'value': 2, 'text': 'Limited experimentation with basic tools'},
                {'value': 3, 'text': 'Some experience with standard AI platforms'},
                {'value': 4, 'text': 'Good experience across multiple AI tools'},
                {'value': 5, 'text': 'Advanced AI/ML capabilities with custom solutions'}
            ]
        }
    ],
    'skills': [
        {
            'id': 's1',
            'question': 'What is the level of AI literacy in your organization?',
            'options': [
                {'value': 1, 'text': 'Very low - limited understanding of AI concepts'},
                {'value': 2, 'text': 'Basic awareness but little practical knowledge'},
                {'value': 3, 'text': 'Moderate understanding in key roles'},
                {'value': 4, 'text': 'Good AI literacy across business functions'},
                {'value': 5, 'text': 'High AI fluency with internal expertise'}
            ]
        },
        {
            'id': 's2',
            'question': 'How strong is your technical talent for AI initiatives?',
            'options': [
                {'value': 1, 'text': 'No dedicated AI technical talent'},
                {'value': 2, 'text': 'Limited technical skills, mostly outsourced'},
                {'value': 3, 'text': 'Some internal technical capabilities'},
                {'value': 4, 'text': 'Strong technical team with AI experience'},
                {'value': 5, 'text': 'World-class AI technical expertise'}
            ]
        }
    ]
}

def calculate_readiness_score(responses):
    """Calculate AI readiness score based on responses"""
    category_scores = {}
    
    for category, category_data in ASSESSMENT_CATEGORIES.items():
        category_responses = [r for r in responses if r['question_id'].startswith(category[0])]
        if category_responses:
            avg_score = sum(r['score'] for r in category_responses) / len(category_responses)
            category_scores[category] = {
                'score': avg_score,
                'weighted_score': avg_score * category_data['weight']
            }
    
    overall_score = sum(cat['weighted_score'] for cat in category_scores.values())
    return overall_score, category_scores

def generate_recommendations(overall_score, category_scores):
    """Generate personalized recommendations based on assessment results"""
    recommendations = []
    
    if overall_score < 2.0:
        recommendations.append({
            'priority': 'Critical',
            'category': 'Foundation',
            'title': 'Establish AI Foundation',
            'description': 'Focus on building basic AI awareness and securing leadership commitment before pursuing specific initiatives.',
            'actions': [
                'Conduct AI literacy sessions for leadership team',
                'Develop initial AI strategy and vision',
                'Identify quick wins to build confidence'
            ]
        })
    
    # Category-specific recommendations
    for category, score_data in category_scores.items():
        if score_data['score'] < 3.0:
            category_info = ASSESSMENT_CATEGORIES[category]
            if category == 'leadership':
                recommendations.append({
                    'priority': 'High',
                    'category': category_info['name'],
                    'title': 'Strengthen Leadership Alignment',
                    'description': 'Build stronger executive support and strategic integration of AI initiatives.',
                    'actions': [
                        'Develop comprehensive AI business case',
                        'Create AI steering committee',
                        'Establish clear AI success metrics'
                    ]
                })
            elif category == 'culture':
                recommendations.append({
                    'priority': 'High',
                    'category': category_info['name'],
                    'title': 'Foster Experimentation Culture',
                    'description': 'Build organizational capacity for learning and iterating with AI technologies.',
                    'actions': [
                        'Implement "fail fast, learn faster" approach',
                        'Create cross-functional AI innovation teams',
                        'Establish regular AI learning sessions'
                    ]
                })
            elif category == 'data':
                recommendations.append({
                    'priority': 'Medium',
                    'category': category_info['name'],
                    'title': 'Improve Data Infrastructure',
                    'description': 'Enhance data quality and accessibility for AI applications.',
                    'actions': [
                        'Conduct data audit and quality assessment',
                        'Implement data integration platform',
                        'Establish data governance framework'
                    ]
                })
    
    return recommendations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html', 
                         categories=ASSESSMENT_CATEGORIES,
                         questions=ASSESSMENT_QUESTIONS)

@app.route('/api/submit_assessment', methods=['POST'])
def submit_assessment():
    data = request.get_json()
    responses = data.get('responses', [])
    company_info = data.get('company_info', {})
    
    # Calculate scores
    overall_score, category_scores = calculate_readiness_score(responses)
    
    # Generate recommendations
    recommendations = generate_recommendations(overall_score, category_scores)
    
    # Store results in session
    assessment_id = str(uuid.uuid4())
    session[assessment_id] = {
        'company_info': company_info,
        'responses': responses,
        'overall_score': overall_score,
        'category_scores': category_scores,
        'recommendations': recommendations,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'assessment_id': assessment_id,
        'overall_score': round(overall_score, 2),
        'category_scores': {k: round(v['score'], 2) for k, v in category_scores.items()},
        'recommendations': recommendations
    })

@app.route('/results/<assessment_id>')
def results(assessment_id):
    if assessment_id not in session:
        return redirect('/')
    
    assessment_data = session[assessment_id]
    return render_template('results.html', 
                         assessment=assessment_data,
                         categories=ASSESSMENT_CATEGORIES)

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/resources/data-preparation')
def data_preparation():
    return render_template('data_preparation.html')

@app.route('/resources/technology-stack')
def technology_stack():
    return render_template('technology_stack.html')

@app.route('/resources/privacy-data-rights')
def privacy_data_rights():
    return render_template('privacy_data_rights.html')

@app.route('/resources/ai-strategy-framework')
def ai_strategy_framework():
    return render_template('ai_strategy_framework.html')

# Export the Flask app for Vercel
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)