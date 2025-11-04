"""
LiteLLM WebUI Client
A web interface that communicates with the LiteLLM API Service
Runs on port 5500
"""
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Configuration
LITELLM_API_URL = os.getenv('LITELLM_API_URL', 'http://localhost:5000')
APPLICATION_ID = 'litellm-webui'

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html', api_url=LITELLM_API_URL)

@app.route('/usage')
def usage_page():
    """Render the usage statistics page"""
    return render_template('usage.html', api_url=LITELLM_API_URL)

@app.route('/api/proxy/models', methods=['GET'])
def proxy_models():
    """Proxy request to get models from LiteLLM service"""
    try:
        response = requests.get(f'{LITELLM_API_URL}/api/models')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proxy/chat', methods=['POST'])
def proxy_chat():
    """Proxy chat request to LiteLLM service"""
    try:
        data = request.json
        # Add application_id to the request
        data['application_id'] = APPLICATION_ID
        
        response = requests.post(
            f'{LITELLM_API_URL}/api/chat',
            json=data,
            timeout=120
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proxy/user/<user_id>/usage', methods=['GET'])
def proxy_user_usage(user_id):
    """Proxy request to get user usage from LiteLLM service"""
    try:
        response = requests.get(f'{LITELLM_API_URL}/api/user/{user_id}/usage')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proxy/stats', methods=['GET'])
def proxy_stats():
    """Proxy request to get global stats from LiteLLM service"""
    try:
        response = requests.get(f'{LITELLM_API_URL}/api/stats')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🌐 LiteLLM WebUI Starting...")
    print("=" * 60)
    print(f"📍 Running on: http://localhost:5500")
    print(f"🔗 API Service: {LITELLM_API_URL}")
    print(f"🎨 Open your browser to: http://localhost:5500")
    print("=" * 60)
    app.run(debug=True, port=5500, host='0.0.0.0')

