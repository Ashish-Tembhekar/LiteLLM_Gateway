"""
LiteLLM API Service
A microservice that handles LLM requests and tracks usage in SQLite database
Runs on port 5000
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from litellm import completion
import time
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv
import json
import uuid

# Load environment variables
load_dotenv(dotenv_path='../.env')

app = Flask(__name__)
CORS(app)  # Enable CORS for WebUI to call this service

# Database configuration
DB_PATH = 'litellm_usage.db'

def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for storing all requests and responses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id TEXT PRIMARY KEY,
            application_id TEXT,
            user_id TEXT,
            model TEXT NOT NULL,
            query TEXT NOT NULL,
            response TEXT,
            response_time REAL,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_tokens INTEGER,
            cost_usd REAL,
            timestamp TEXT NOT NULL,
            status TEXT,
            error_message TEXT
        )
    ''')
    
    # Index for faster user queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_user_id ON requests(user_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_application_id ON requests(application_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timestamp ON requests(timestamp)
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Approximate token costs (USD per 1K tokens) - Update these based on current pricing
TOKEN_COSTS = {
    'gpt-4o': {'input': 0.0025, 'output': 0.01},
    'gpt-4o-mini': {'input': 0.00015, 'output': 0.0006},
    'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
    'gpt-4': {'input': 0.03, 'output': 0.06},
    'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
    'claude-3-5-sonnet-20241022': {'input': 0.003, 'output': 0.015},
    'claude-3-5-haiku-20241022': {'input': 0.0008, 'output': 0.004},
    'claude-3-opus-20240229': {'input': 0.015, 'output': 0.075},
    'gemini/gemini-1.5-pro': {'input': 0.00125, 'output': 0.005},
    'gemini/gemini-1.5-flash': {'input': 0.000075, 'output': 0.0003},
    'groq/llama-3.3-70b-versatile': {'input': 0.00059, 'output': 0.00079},
    'groq/llama-3.1-70b-versatile': {'input': 0.00059, 'output': 0.00079},
    'groq/llama-3.1-8b-instant': {'input': 0.00005, 'output': 0.00008},
}

def calculate_cost(model, prompt_tokens, completion_tokens):
    """Calculate approximate cost in USD"""
    if model in TOKEN_COSTS:
        costs = TOKEN_COSTS[model]
        input_cost = (prompt_tokens / 1000) * costs['input']
        output_cost = (completion_tokens / 1000) * costs['output']
        return round(input_cost + output_cost, 6)
    return 0.0

def save_request_to_db(request_data):
    """Save request and response data to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO requests (
            id, application_id, user_id, model, query, response,
            response_time, prompt_tokens, completion_tokens, total_tokens,
            cost_usd, timestamp, status, error_message
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        request_data['id'],
        request_data.get('application_id'),
        request_data.get('user_id'),
        request_data['model'],
        request_data['query'],
        request_data.get('response'),
        request_data.get('response_time'),
        request_data.get('prompt_tokens'),
        request_data.get('completion_tokens'),
        request_data.get('total_tokens'),
        request_data.get('cost_usd'),
        request_data['timestamp'],
        request_data['status'],
        request_data.get('error_message')
    ))
    
    conn.commit()
    conn.close()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'LiteLLM API Service',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get list of available models"""
    models = {
        "OpenAI": [
            {"id": "gpt-4o", "name": "GPT-4o", "provider": "openai"},
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "openai"},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "provider": "openai"},
            {"id": "gpt-4", "name": "GPT-4", "provider": "openai"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "openai"},
        ],
        "Anthropic": [
            {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet", "provider": "anthropic"},
            {"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku", "provider": "anthropic"},
            {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "provider": "anthropic"},
        ],
        "Google Gemini": [
            {"id": "gemini/gemini-2.0-flash-exp", "name": "Gemini 2.0 Flash", "provider": "google"},
            {"id": "gemini/gemini-1.5-pro", "name": "Gemini 1.5 Pro", "provider": "google"},
            {"id": "gemini/gemini-1.5-flash", "name": "Gemini 1.5 Flash", "provider": "google"},
        ],
        "Groq": [
            {"id": "groq/llama-3.3-70b-versatile", "name": "Llama 3.3 70B", "provider": "groq"},
            {"id": "groq/llama-3.1-70b-versatile", "name": "Llama 3.1 70B", "provider": "groq"},
            {"id": "groq/llama-3.1-8b-instant", "name": "Llama 3.1 8B", "provider": "groq"},
            {"id": "groq/mixtral-8x7b-32768", "name": "Mixtral 8x7B", "provider": "groq"},
        ],
    }
    return jsonify(models)

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main endpoint for LLM chat requests
    
    Request body:
    {
        "application_id": "web-ui",  // optional
        "user_id": "user123",        // optional
        "query": "What is AI?",      // required
        "model": "gpt-4o"            // required
    }
    """
    data = request.json
    
    # Validate required fields
    if not data or 'query' not in data or 'model' not in data:
        return jsonify({
            'error': 'Missing required fields: query and model are required'
        }), 400
    
    # Generate unique request ID
    request_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Extract request data
    application_id = data.get('application_id', 'unknown')
    user_id = data.get('user_id', 'anonymous')
    query = data.get('query')
    model = data.get('model')
    
    # Prepare request data for database
    request_data = {
        'id': request_id,
        'application_id': application_id,
        'user_id': user_id,
        'model': model,
        'query': query,
        'timestamp': timestamp,
        'status': 'pending'
    }
    
    try:
        # Make LLM request
        start_time = time.time()
        
        response = completion(
            model=model,
            messages=[{"role": "user", "content": query}]
        )
        
        end_time = time.time()
        response_time = round(end_time - start_time, 3)
        
        # Extract response data
        content = response.choices[0].message.content
        usage = response.usage
        
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens
        
        # Calculate cost
        cost_usd = calculate_cost(model, prompt_tokens, completion_tokens)
        
        # Update request data with response
        request_data.update({
            'response': content,
            'response_time': response_time,
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': total_tokens,
            'cost_usd': cost_usd,
            'status': 'success'
        })
        
        # Save to database
        save_request_to_db(request_data)
        
        # Return response
        return jsonify({
            'request_id': request_id,
            'response': content,
            'metadata': {
                'response_time': response_time,
                'tokens': {
                    'prompt': prompt_tokens,
                    'completion': completion_tokens,
                    'total': total_tokens
                },
                'cost_usd': cost_usd,
                'timestamp': timestamp,
                'model': model,
                'application_id': application_id,
                'user_id': user_id
            }
        })
        
    except Exception as e:
        # Log error to database
        request_data.update({
            'status': 'error',
            'error_message': str(e)
        })
        save_request_to_db(request_data)
        
        return jsonify({
            'request_id': request_id,
            'error': str(e),
            'timestamp': timestamp
        }), 500

@app.route('/api/user/<user_id>/usage', methods=['GET'])
def get_user_usage(user_id):
    """
    Get usage statistics for a specific user
    
    Returns all requests made by the user with aggregated statistics
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    cursor = conn.cursor()
    
    # Get all requests for this user
    cursor.execute('''
        SELECT * FROM requests 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    ''', (user_id,))
    
    requests = [dict(row) for row in cursor.fetchall()]
    
    # Calculate aggregate statistics
    cursor.execute('''
        SELECT 
            COUNT(*) as total_requests,
            SUM(total_tokens) as total_tokens,
            SUM(prompt_tokens) as total_prompt_tokens,
            SUM(completion_tokens) as total_completion_tokens,
            SUM(cost_usd) as total_cost_usd,
            AVG(response_time) as avg_response_time,
            COUNT(DISTINCT application_id) as apps_used,
            COUNT(DISTINCT model) as models_used
        FROM requests 
        WHERE user_id = ? AND status = 'success'
    ''', (user_id,))
    
    stats = dict(cursor.fetchone())
    
    # Get usage by application
    cursor.execute('''
        SELECT 
            application_id,
            COUNT(*) as request_count,
            SUM(total_tokens) as tokens,
            SUM(cost_usd) as cost
        FROM requests 
        WHERE user_id = ? AND status = 'success'
        GROUP BY application_id
    ''', (user_id,))
    
    usage_by_app = [dict(row) for row in cursor.fetchall()]
    
    # Get usage by model
    cursor.execute('''
        SELECT 
            model,
            COUNT(*) as request_count,
            SUM(total_tokens) as tokens,
            SUM(cost_usd) as cost
        FROM requests 
        WHERE user_id = ? AND status = 'success'
        GROUP BY model
    ''', (user_id,))
    
    usage_by_model = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'user_id': user_id,
        'summary': {
            'total_requests': stats['total_requests'] or 0,
            'total_tokens': stats['total_tokens'] or 0,
            'total_prompt_tokens': stats['total_prompt_tokens'] or 0,
            'total_completion_tokens': stats['total_completion_tokens'] or 0,
            'total_cost_usd': round(stats['total_cost_usd'] or 0, 4),
            'avg_response_time': round(stats['avg_response_time'] or 0, 3),
            'apps_used': stats['apps_used'] or 0,
            'models_used': stats['models_used'] or 0
        },
        'usage_by_application': usage_by_app,
        'usage_by_model': usage_by_model,
        'recent_requests': requests[:50]  # Return last 50 requests
    })

@app.route('/api/stats', methods=['GET'])
def get_global_stats():
    """Get global usage statistics across all users"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total_requests,
            COUNT(DISTINCT user_id) as unique_users,
            COUNT(DISTINCT application_id) as unique_apps,
            SUM(total_tokens) as total_tokens,
            SUM(cost_usd) as total_cost_usd
        FROM requests 
        WHERE status = 'success'
    ''')
    
    stats = dict(cursor.fetchone())
    conn.close()
    
    return jsonify(stats)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 LiteLLM API Service Starting...")
    print("=" * 60)
    print(f"📍 Running on: http://localhost:5000")
    print(f"💾 Database: {DB_PATH}")
    print(f"🔗 Endpoints:")
    print(f"   - POST /api/chat - Make LLM requests")
    print(f"   - GET  /api/user/<user_id>/usage - Get user usage stats")
    print(f"   - GET  /api/models - Get available models")
    print(f"   - GET  /api/stats - Get global statistics")
    print(f"   - GET  /health - Health check")
    print("=" * 60)
    app.run(debug=True, port=5000, host='0.0.0.0')

