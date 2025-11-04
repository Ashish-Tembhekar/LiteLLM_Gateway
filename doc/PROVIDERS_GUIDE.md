# LiteLLM Chat App - Supported Providers Guide

This guide lists all the LLM providers supported by the LiteLLM Chat App and how to get started with each.

## 🚀 Quick Start Providers (Free Tiers Available)

### 1. **Groq** ⚡ (Recommended for beginners)
- **Why**: Extremely fast, generous free tier
- **Models**: Llama 3.3 70B, Llama 3.1, Mixtral, Gemma 2
- **Get API Key**: https://console.groq.com/keys
- **Free Tier**: Yes, very generous
- **Env Variable**: `GROQ_API_KEY`

### 2. **Google Gemini** 🌟
- **Why**: Powerful models, free tier available
- **Models**: Gemini 2.0 Flash, Gemini 1.5 Pro/Flash
- **Get API Key**: https://aistudio.google.com/apikey
- **Free Tier**: Yes, 60 requests/minute
- **Env Variable**: `GOOGLE_API_KEY`

### 3. **Ollama** 🏠 (100% Free - Local)
- **Why**: Run models locally, completely free, no API key needed
- **Models**: Llama 3.1, Mistral, Code Llama, Phi-3, and more
- **Setup**: Install from https://ollama.ai
- **Free Tier**: Yes, runs on your machine
- **Env Variable**: `OLLAMA_API_BASE` (default: http://localhost:11434)

## 💰 Premium Providers

### 4. **OpenAI** 🤖
- **Models**: GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo, O1 models
- **Get API Key**: https://platform.openai.com/api-keys
- **Pricing**: Pay-per-use, starts at $0.002/1K tokens
- **Env Variable**: `OPENAI_API_KEY`

### 5. **Anthropic (Claude)** 🧠
- **Models**: Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3 Opus
- **Get API Key**: https://console.anthropic.com/settings/keys
- **Pricing**: Pay-per-use, competitive pricing
- **Env Variable**: `ANTHROPIC_API_KEY`

### 6. **Mistral AI** 🇫🇷
- **Models**: Mistral Large, Medium, Small, Codestral
- **Get API Key**: https://console.mistral.ai/api-keys
- **Pricing**: Pay-per-use, European provider
- **Env Variable**: `MISTRAL_API_KEY`

### 7. **Perplexity AI** 🔍
- **Models**: Sonar models with online search capabilities
- **Get API Key**: https://www.perplexity.ai/settings/api
- **Pricing**: Pay-per-use, includes web search
- **Env Variable**: `PERPLEXITYAI_API_KEY`

### 8. **DeepSeek** 🇨🇳
- **Models**: DeepSeek Chat, DeepSeek Coder
- **Get API Key**: https://platform.deepseek.com/api_keys
- **Pricing**: Very competitive pricing
- **Env Variable**: `DEEPSEEK_API_KEY`

### 9. **xAI (Grok)** 🚀
- **Models**: Grok Beta, Grok Vision Beta
- **Get API Key**: https://console.x.ai/
- **Pricing**: Pay-per-use
- **Env Variable**: `XAI_API_KEY`

## 🌐 Model Aggregators

### 10. **OpenRouter** 🔀
- **Why**: Access 100+ models through one API
- **Models**: GPT-4, Claude, Llama, and many more
- **Get API Key**: https://openrouter.ai/keys
- **Pricing**: Varies by model, competitive rates
- **Env Variable**: `OPENROUTER_API_KEY`

### 11. **Together AI** 🤝
- **Models**: Llama 3, Mixtral, and many open-source models
- **Get API Key**: https://api.together.xyz/settings/api-keys
- **Pricing**: Pay-per-use, good for open-source models
- **Env Variable**: `TOGETHERAI_API_KEY`

### 12. **Replicate** 🔁
- **Models**: Various open-source models (Llama 2, Mixtral, etc.)
- **Get API Key**: https://replicate.com/account/api-tokens
- **Pricing**: Pay-per-use, per-second billing
- **Env Variable**: `REPLICATE_API_KEY`

### 13. **Fireworks AI** 🎆
- **Models**: Fast inference for Llama 3.1, Mixtral, and more
- **Get API Key**: https://fireworks.ai/api-keys
- **Pricing**: Pay-per-use, optimized for speed
- **Env Variable**: `FIREWORKS_API_KEY`

## ☁️ Cloud Platform Providers

### 14. **Azure OpenAI** ☁️
- **Models**: GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo
- **Setup**: https://portal.azure.com
- **Pricing**: Enterprise pricing, SLA guarantees
- **Env Variables**: `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION`

### 15. **AWS Bedrock** 🪨
- **Models**: Claude, Llama, Mistral, and more on AWS
- **Setup**: AWS Console
- **Pricing**: AWS pricing, enterprise features
- **Env Variables**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION_NAME`

### 16. **Google Vertex AI** 🔺
- **Models**: Gemini, Claude on Google Cloud
- **Setup**: https://cloud.google.com/vertex-ai
- **Pricing**: GCP pricing, enterprise features
- **Env Variables**: `GOOGLE_APPLICATION_CREDENTIALS`, `VERTEX_PROJECT`, `VERTEX_LOCATION`

## 🛠️ Developer Platforms

### 17. **Hugging Face** 🤗
- **Models**: Thousands of open-source models
- **Get API Key**: https://huggingface.co/settings/tokens
- **Pricing**: Free tier + paid inference
- **Env Variable**: `HUGGINGFACE_API_KEY`

### 18. **Anyscale** 📡
- **Models**: Llama 3, Mixtral, optimized inference
- **Get API Key**: https://app.endpoints.anyscale.com/credentials
- **Pricing**: Pay-per-use
- **Env Variable**: `ANYSCALE_API_KEY`

### 19. **Cohere** 🎯
- **Models**: Command R+, Command R, Command
- **Get API Key**: https://dashboard.cohere.com/api-keys
- **Pricing**: Free tier + paid plans
- **Env Variable**: `COHERE_API_KEY`

### 20. **AI21** 🦾
- **Models**: Jurassic-2 Ultra, Jurassic-2 Mid
- **Get API Key**: https://studio.ai21.com/account/api-key
- **Pricing**: Pay-per-use
- **Env Variable**: `AI21_API_KEY`

## 📋 Setup Instructions

### Step 1: Choose Your Providers
Pick one or more providers from the list above based on:
- **Budget**: Start with free tiers (Groq, Gemini, Ollama)
- **Use Case**: Different models excel at different tasks
- **Speed**: Groq and Fireworks AI are fastest
- **Quality**: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro are top-tier

### Step 2: Get API Keys
1. Visit the provider's website (links above)
2. Sign up for an account
3. Navigate to API keys section
4. Generate a new API key
5. Copy the key (you usually can't see it again!)

### Step 3: Configure Environment
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```bash
   # Example
   OPENAI_API_KEY=sk-proj-xxxxx
   GROQ_API_KEY=gsk_xxxxx
   GOOGLE_API_KEY=AIzaSyxxxxx
   ```

3. Save the file

### Step 4: Start the App
```bash
cd chat_app
python app.py
```

### Step 5: Test Your Models
1. Open http://localhost:5000
2. Select a model from the sidebar
3. Send a test message
4. Compare response times and quality!

## 💡 Tips & Best Practices

### Cost Optimization
- **Start Free**: Use Groq, Gemini, or Ollama for testing
- **Compare Prices**: Different providers charge different rates
- **Use Smaller Models**: GPT-3.5, Claude Haiku, Gemini Flash are cheaper
- **Monitor Usage**: Set up billing alerts on provider dashboards

### Performance
- **Fastest**: Groq (sub-second responses)
- **Best Quality**: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro
- **Best Value**: Groq (free + fast), DeepSeek (cheap + good)
- **Local**: Ollama (no latency, no cost, privacy)

### Security
- **Never commit** `.env` files to git
- **Rotate keys** regularly
- **Use environment variables** in production
- **Set spending limits** on provider dashboards
- **Monitor usage** for unexpected spikes

### Model Selection Guide
- **General Chat**: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro
- **Coding**: Claude 3.5 Sonnet, GPT-4o, DeepSeek Coder, Codestral
- **Fast Responses**: Groq models, Gemini Flash
- **Long Context**: Claude (200K), Gemini 1.5 Pro (2M tokens)
- **Cost-Effective**: Groq (free), DeepSeek, GPT-3.5 Turbo
- **Privacy**: Ollama (local), Azure/Bedrock (enterprise)

## 🆘 Troubleshooting

### "API key not valid"
- Check if the key is correctly copied (no extra spaces)
- Verify the key hasn't expired
- Ensure you have credits/quota remaining

### "Model not found"
- Check if the model name is correct in `app.py`
- Some models may not be available in your region
- Verify your account has access to that model

### "Rate limit exceeded"
- You've hit the provider's rate limit
- Wait a few minutes or upgrade your plan
- Try a different provider

### Connection errors
- Check your internet connection
- Verify the provider's service status
- Check if you need to configure proxy settings

## 🔗 Useful Links

- **LiteLLM Docs**: https://docs.litellm.ai/
- **Model Pricing**: https://litellm.ai/pricing
- **Provider Status**: Check individual provider status pages
- **Community**: https://discord.gg/litellm

## 📊 Provider Comparison Table

| Provider | Free Tier | Speed | Quality | Best For |
|----------|-----------|-------|---------|----------|
| Groq | ✅ Generous | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Fast responses |
| Gemini | ✅ Yes | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Multimodal, long context |
| Ollama | ✅ Unlimited | ⚡⚡⚡ | ⭐⭐⭐⭐ | Privacy, offline use |
| OpenAI | ❌ No | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | General purpose |
| Anthropic | ❌ No | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Coding, analysis |
| DeepSeek | ❌ No | ⚡⚡⚡⭐ | ⭐⭐⭐⭐ | Cost-effective coding |
| Perplexity | ❌ No | ⚡⚡⚡ | ⭐⭐⭐⭐ | Web search + chat |

---

**Ready to get started?** Pick a provider, grab an API key, and start chatting! 🚀

