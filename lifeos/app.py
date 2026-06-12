"""
LifeOS - Life Dashboard Backend
A Flask application for managing personal life metrics and data.
"""

import os
import logging
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', False)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Error handlers
def handle_error(error_code, message):
    """Helper function to create error responses."""
    return jsonify({'error': message, 'code': error_code}), error_code


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.path}")
    return handle_error(404, 'Resource not found')


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 error: {str(error)}")
    return handle_error(500, 'Internal server error')


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors."""
    logger.warning(f"400 error: {str(error)}")
    return handle_error(400, 'Bad request')


# Decorators for validation
def validate_json(*expected_args):
    """Decorator to validate JSON request data."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return handle_error(400, 'Request must be JSON')
            
            data = request.get_json()
            
            # Validate required fields
            for arg in expected_args:
                if arg not in data:
                    return handle_error(400, f'Missing required field: {arg}')
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Routes
@app.route('/')
def index():
    """Serve the main dashboard page."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {str(e)}")
        return handle_error(500, 'Failed to load dashboard')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard data.
    
    Returns:
        JSON object containing dashboard metrics and data
    """
    try:
        dashboard_data = {
            'status': 'success',
            'data': {
                'metrics': [],
                'goals': [],
                'recent_activity': []
            },
            'timestamp': datetime.utcnow().isoformat()
        }
        return jsonify(dashboard_data), 200
    except Exception as e:
        logger.error(f"Error fetching dashboard: {str(e)}")
        return handle_error(500, 'Failed to fetch dashboard data')


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get all metrics.
    
    Query Parameters:
        category (str, optional): Filter by metric category
        limit (int, optional): Limit number of results
    
    Returns:
        JSON array of metrics
    """
    try:
        category = request.args.get('category')
        limit = request.args.get('limit', 10, type=int)
        
        # Validate limit
        if limit <= 0 or limit > 100:
            return handle_error(400, 'Limit must be between 1 and 100')
        
        metrics = {
            'status': 'success',
            'data': [],
            'total': 0,
            'timestamp': datetime.utcnow().isoformat()
        }
        return jsonify(metrics), 200
    except ValueError as e:
        logger.warning(f"Invalid query parameter: {str(e)}")
        return handle_error(400, 'Invalid query parameters')
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        return handle_error(500, 'Failed to fetch metrics')


@app.route('/api/metrics', methods=['POST'])
@validate_json('name', 'value')
def create_metric():
    """Create a new metric.
    
    Request body:
        {
            "name": "metric_name",
            "value": 100,
            "category": "health"  (optional),
            "timestamp": "2024-01-01T12:00:00"  (optional)
        }
    
    Returns:
        Created metric object
    """
    try:
        data = request.get_json()
        
        # Validate data types
        if not isinstance(data.get('value'), (int, float)):
            return handle_error(400, 'Value must be a number')
        
        created_metric = {
            'status': 'success',
            'message': 'Metric created successfully',
            'data': {
                'id': 1,
                'name': data.get('name'),
                'value': data.get('value'),
                'category': data.get('category', 'general'),
                'timestamp': data.get('timestamp', datetime.utcnow().isoformat())
            }
        }
        return jsonify(created_metric), 201
    except Exception as e:
        logger.error(f"Error creating metric: {str(e)}")
        return handle_error(500, 'Failed to create metric')


@app.route('/api/goals', methods=['GET'])
def get_goals():
    """Get all goals.
    
    Returns:
        JSON array of goals
    """
    try:
        goals = {
            'status': 'success',
            'data': [],
            'total': 0,
            'timestamp': datetime.utcnow().isoformat()
        }
        return jsonify(goals), 200
    except Exception as e:
        logger.error(f"Error fetching goals: {str(e)}")
        return handle_error(500, 'Failed to fetch goals')


@app.route('/api/goals', methods=['POST'])
@validate_json('title', 'target')
def create_goal():
    """Create a new goal.
    
    Request body:
        {
            "title": "goal_title",
            "target": 100,
            "category": "health",  (optional)
            "deadline": "2024-12-31"  (optional)
        }
    
    Returns:
        Created goal object
    """
    try:
        data = request.get_json()
        
        created_goal = {
            'status': 'success',
            'message': 'Goal created successfully',
            'data': {
                'id': 1,
                'title': data.get('title'),
                'target': data.get('target'),
                'current': 0,
                'category': data.get('category', 'general'),
                'deadline': data.get('deadline'),
                'created_at': datetime.utcnow().isoformat()
            }
        }
        return jsonify(created_goal), 201
    except Exception as e:
        logger.error(f"Error creating goal: {str(e)}")
        return handle_error(500, 'Failed to create goal')


if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting LifeOS server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
