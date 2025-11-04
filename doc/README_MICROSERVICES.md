# LiteLLM Microservices Architecture

A production-ready microservices setup with separate API service and WebUI client.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Browser                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    WebUI (Port 5500)                         │
│  - Flask web server                                          │
│  - Serves HTML/CSS/JS                                        │
│  - Proxies requests to API service                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                LiteLLM API Service (Port 5000)               │
│  - Flask REST API                                            │
│  - Handles LLM requests via LiteLLM                          │
│  - SQLite database for tracking                              │
│  - Token counting & cost calculation                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ API Calls
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              LLM Providers (OpenAI, Anthropic, etc.)         │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
litellm-crash-course/
├── litellm_service/          # API Service (Port 5000)
│   ├── api_service.py        # Main Flask API
│   ├── requirements.txt      # Python dependencies
│   └── litellm_usage.db      # SQLite database (auto-created)
│
├── webui/                    # WebUI Client (Port 5500)
│   ├── app.py                # Flask web server
│   ├── requirements.txt      # Python dependencies
│   └── templates/
│       ├── index.html        # Chat interface
│       └── usage.html        # Usage statistics page
│
└── .env                      # API keys (shared)
```

## 🚀 Quick Start

### Step 1: Install Dependencies

**For API Service:**
```bash
cd litellm_service
pip install -r requirements.txt
```

**For WebUI:**
```bash
cd webui
pip install -r requirements.txt
```

Or install both at once from the root:
```bash
pip install -r litellm_service/requirements.txt
pip install -r webui/requirements.txt
```

### Step 2: Configure API Keys

Make sure your `.env` file in the root directory has the required API keys:
```bash
OPENAI_API_KEY=sk-proj-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
GOOGLE_API_KEY=AIzaSyxxxxx
GROQ_API_KEY=gsk_xxxxx
# ... add other providers as needed
```

### Step 3: Start the Services

**Terminal 1 - Start API Service:**
```bash
cd litellm_service
python api_service.py
```

**Terminal 2 - Start WebUI:**
```bash
cd webui
python app.py
```

### Step 4: Access the Application

- **WebUI**: http://localhost:5500
- **API Service**: http://localhost:5000
- **Usage Stats**: http://localhost:5500/usage

## 📡 API Endpoints

### LiteLLM API Service (Port 5000)

#### 1. **POST /api/chat** - Make LLM Request
Request:
```json
{
  "application_id": "my-app",     // optional
  "user_id": "user123",           // optional
  "query": "What is AI?",         // required
  "model": "gpt-4o"               // required
}
```

Response:
```json
{
  "request_id": "uuid-here",
  "response": "AI is...",
  "metadata": {
    "response_time": 1.234,
    "tokens": {
      "prompt": 10,
      "completion": 50,
      "total": 60
    },
    "cost_usd": 0.00015,
    "timestamp": "2025-11-03T12:00:00",
    "model": "gpt-4o",
    "application_id": "my-app",
    "user_id": "user123"
  }
}
```

#### 2. **GET /api/user/{user_id}/usage** - Get User Statistics
Response:
```json
{
  "user_id": "user123",
  "summary": {
    "total_requests": 100,
    "total_tokens": 50000,
    "total_cost_usd": 0.5,
    "avg_response_time": 1.5,
    "apps_used": 2,
    "models_used": 3
  },
  "usage_by_application": [...],
  "usage_by_model": [...],
  "recent_requests": [...]
}
```

#### 3. **GET /api/models** - Get Available Models
Returns list of all available models grouped by provider.

#### 4. **GET /api/stats** - Get Global Statistics
Returns aggregate statistics across all users.

#### 5. **GET /health** - Health Check
Returns service health status.

## 💾 Database Schema

The API service uses SQLite with the following schema:

```sql
CREATE TABLE requests (
    id TEXT PRIMARY KEY,              -- Unique request ID
    application_id TEXT,              -- Which app made the request
    user_id TEXT,                     -- Which user made the request
    model TEXT NOT NULL,              -- Model used
    query TEXT NOT NULL,              -- User's query
    response TEXT,                    -- LLM's response
    response_time REAL,               -- Time taken (seconds)
    prompt_tokens INTEGER,            -- Input tokens
    completion_tokens INTEGER,        -- Output tokens
    total_tokens INTEGER,             -- Total tokens
    cost_usd REAL,                    -- Estimated cost
    timestamp TEXT NOT NULL,          -- When request was made
    status TEXT,                      -- success/error
    error_message TEXT                -- Error details if failed
);
```

## 🔧 Configuration

### Environment Variables

**API Service:**
- All LLM provider API keys (see `.env.example`)

**WebUI:**
- `LITELLM_API_URL` - URL of API service (default: http://localhost:5000)

### Changing Ports

**API Service** - Edit `litellm_service/api_service.py`:
```python
app.run(debug=True, port=5000, host='0.0.0.0')  # Change 5000 to your port
```

**WebUI** - Edit `webui/app.py`:
```python
app.run(debug=True, port=5500, host='0.0.0.0')  # Change 5500 to your port
```

## 📊 Features

### API Service Features
- ✅ Request/Response tracking in SQLite
- ✅ Token counting and cost calculation
- ✅ User-based usage statistics
- ✅ Application-based tracking
- ✅ Model performance metrics
- ✅ Error logging and handling
- ✅ CORS enabled for WebUI access
- ✅ RESTful API design

### WebUI Features
- ✅ Beautiful, modern chat interface
- ✅ Real-time API connection status
- ✅ User ID customization
- ✅ Model selection from all providers
- ✅ Response time display
- ✅ Token usage display
- ✅ Cost tracking per message
- ✅ Request ID tracking
- ✅ Comprehensive usage statistics page
- ✅ Usage breakdown by app and model
- ✅ Recent requests history

## 🧪 Testing the API

### Using cURL

**Make a chat request:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "application_id": "curl-test",
    "query": "Hello, how are you?",
    "model": "gpt-3.5-turbo"
  }'
```

**Get user statistics:**
```bash
curl http://localhost:5000/api/user/test-user/usage
```

**Get available models:**
```bash
curl http://localhost:5000/api/models
```

### Using Python

```python
import requests

# Make a chat request
response = requests.post('http://localhost:5000/api/chat', json={
    'user_id': 'python-user',
    'application_id': 'python-script',
    'query': 'What is machine learning?',
    'model': 'gpt-4o'
})

data = response.json()
print(f"Response: {data['response']}")
print(f"Cost: ${data['metadata']['cost_usd']}")
print(f"Tokens: {data['metadata']['tokens']['total']}")

# Get user stats
stats = requests.get('http://localhost:5000/api/user/python-user/usage').json()
print(f"Total requests: {stats['summary']['total_requests']}")
print(f"Total cost: ${stats['summary']['total_cost_usd']}")
```

## 🔒 Security Considerations

### For Production Deployment:

1. **API Authentication**: Add API key authentication to the API service
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **HTTPS**: Use HTTPS for both services
4. **Database**: Consider PostgreSQL for production instead of SQLite
5. **Environment Variables**: Use proper secret management
6. **CORS**: Restrict CORS to specific origins
7. **Input Validation**: Add comprehensive input validation
8. **Logging**: Implement proper logging and monitoring

## 📈 Monitoring & Analytics

The system tracks:
- Total requests per user
- Token usage per user/app/model
- Cost per user/app/model
- Average response times
- Error rates
- Model usage patterns

Access statistics at: http://localhost:5500/usage

## 🐛 Troubleshooting

### API Service won't start
- Check if port 5000 is already in use
- Verify API keys are set in `.env`
- Check Python dependencies are installed

### WebUI can't connect to API
- Ensure API service is running on port 5000
- Check CORS is enabled in API service
- Verify `LITELLM_API_URL` is correct

### Database errors
- Delete `litellm_usage.db` to reset database
- Check file permissions
- Ensure SQLite is available

### LLM requests failing
- Verify API keys are valid
- Check provider service status
- Review error messages in API response

## 🚢 Deployment

### Docker Deployment (Recommended)

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  api:
    build: ./litellm_service
    ports:
      - "5000:5000"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
  
  webui:
    build: ./webui
    ports:
      - "5500:5500"
    environment:
      - LITELLM_API_URL=http://api:5000
    depends_on:
      - api
```

### Cloud Deployment
- **API Service**: Deploy to AWS Lambda, Google Cloud Run, or Azure Functions
- **WebUI**: Deploy to Vercel, Netlify, or any static hosting
- **Database**: Use managed PostgreSQL (AWS RDS, Google Cloud SQL)

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

**Built with ❤️ using LiteLLM, Flask, and SQLite**

