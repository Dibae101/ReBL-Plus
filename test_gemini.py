#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Check if API key exists
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("GEMINI_API_KEY not found in environment variables")
    print("\nPlease set your API key in one of these ways:")
    print("1. Create a .env file with: GEMINI_API_KEY=your-key-here")
    print("2. Export in terminal: export GEMINI_API_KEY=your-key-here")
    exit(1)

print(f"GEMINI_API_KEY found (length: {len(api_key)} chars)")

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    print("Gemini API configured successfully")
except Exception as e:
    print(f"Failed to configure Gemini API: {e}")
    exit(1)

# Test with Gemini Pro
try:
    print("\nTesting Gemini 2.0 Flash model...")
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content("Say 'Hello' in one word")
    print(f"Gemini 2.0 Flash response: {response.text.strip()}")
except Exception as e:
    print(f"Gemini 2.0 Flash test failed: {e}")

# Test with Gemini Pro
try:
    print("\nTesting Gemini Pro model...")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say 'Hello' in one word")
    print(f" Gemini Pro response: {response.text.strip()}")
except Exception as e:
    print(f" Gemini Pro test failed: {e}")

# Try Gemini 1.5 Pro
try:
    print("\n Testing Gemini 1.5 Pro model...")
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content("Say 'Hello' in one word")
    print(f" Gemini 1.5 Pro response: {response.text.strip()}")
except Exception as e:
    print(f" Gemini 1.5 Pro test failed: {e}")

print("\n✨ API key test complete!")
