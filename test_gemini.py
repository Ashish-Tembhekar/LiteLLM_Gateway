"""
Test script to verify Gemini API is working with LiteLLM
"""
from litellm import completion
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_gemini():
    """Test if Gemini API is working"""
    
    # Check if API key exists
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in .env file")
        return False
    
    print(f"✓ Found GOOGLE_API_KEY: {api_key[:10]}...")
    print("\n🧪 Testing Gemini API with LiteLLM...\n")
    
    try:
        # Test with Gemini 1.5 Flash (fastest model)
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[
                {"role": "user", "content": "Say 'Hello! Gemini is working!' in a friendly way."}
            ]
        )
        
        # Extract response
        content = response.choices[0].message.content
        tokens = response.usage
        
        print("✅ SUCCESS! Gemini API is working!\n")
        print(f"📝 Response: {content}\n")
        print(f"📊 Token Usage:")
        print(f"   - Prompt tokens: {tokens.prompt_tokens}")
        print(f"   - Completion tokens: {tokens.completion_tokens}")
        print(f"   - Total tokens: {tokens.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Gemini API test failed!")
        print(f"   Error message: {str(e)}\n")
        
        # Provide helpful debugging info
        if "API key not valid" in str(e) or "invalid" in str(e).lower():
            print("💡 Tip: Your API key might be invalid or expired.")
            print("   Get a new key at: https://makersuite.google.com/app/apikey")
        elif "quota" in str(e).lower():
            print("💡 Tip: You might have exceeded your API quota.")
        elif "not found" in str(e).lower():
            print("💡 Tip: The model might not be available in your region.")
        
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  GEMINI API TEST")
    print("=" * 60 + "\n")
    
    success = test_gemini()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Test completed successfully!")
    else:
        print("❌ Test failed. Please check the error above.")
    print("=" * 60)

