import google.generativeai as genai
import datetime
import math
import time 
import json
from utils import *
from dotenv import load_dotenv

# Replace your key here 
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def count_tokens(message):
    # Approximate token count for Gemini (roughly 1 token per 4 characters)
    return len(message) // 4

def count_chat_history_tokens(chat_history):
    total_tokens = 0
    for message in chat_history:
        total_tokens += count_tokens(message['content'])
        total_tokens += count_tokens(message['role'])
    
    return total_tokens

def truncate_message(message, n):
    # Approximate truncation for Gemini
    estimated_tokens = len(message) // 4
    if estimated_tokens <= n:
        return False, None
    else:
        # Truncate to approximate character count
        char_limit = math.floor(n * 4)
        truncated_message = message[:char_limit]
        return True, truncated_message

def process_history(prompt, history, max_tokens, threshold):
    tokens_in_chat_history = count_chat_history_tokens(history)
   
    if tokens_in_chat_history > math.floor(max_tokens*threshold):
        last_prompt_message = history[-1]['content'] 
        if count_tokens(last_prompt_message ) > 4000:
            del history[-1]
            truncated, truncated_message = truncate_message(last_prompt_message, (max_tokens-count_chat_history_tokens(history))*threshold)
            history.append({"role": "user", "content": truncated_message})
        
        print('summarize==========================================')
        history.append({"role": "user", "content": 'The conversation is about to exceed the limit, before we continue the reproduction process. Can you summarize the above conversation. Note that You shouldn\'t summarize the rule and keep the rules as original since the rules are the standards.'})
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        chat_text = convert_history_to_text(history)
        response = model.generate_content(chat_text)
        message = response.text
        print(message)
        history = load_training_prompts('./prompts/training_prompts_ori.json')
        history.append({"role": "user", "content": message})
       
    history.append({"role": "user", "content": prompt})
  
    return history

def convert_history_to_text(history):
    """Convert chat history to a single text prompt for Gemini"""
    text = ""
    for msg in history:
        role = msg['role']
        content = msg['content']
        if role == 'system':
            text += f"System: {content}\n\n"
        elif role == 'user':
            text += f"User: {content}\n\n"
        elif role == 'assistant':
            text += f"Assistant: {content}\n\n"
    return text

def generate_text(prompt, history, package_name=None, model_name="gemini-2.5-flash", max_tokens=128000, attempts = 3):
    
    history = process_history(prompt, history, max_tokens, threshold = 0.75)

    for times in range(attempts):  # retry up to 3 times
        try:
            model = genai.GenerativeModel(model_name)
            chat_text = convert_history_to_text(history)
            
            response = model.generate_content(
                chat_text,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                )
            )
            
            # Create a response object similar to OpenAI format
            formatted_response = {
                "model": model_name,
                "choices": [{"message": {"content": response.text}}]
            }
            return formatted_response, history
        except Exception as e:
            print(f"Attempt {times + 1} failed with error: {str(e)}")
            if times < 2: 
                if package_name is not None:
                    save_chat_history(history, package_name)
                print(f"Take a 60*{times+1} seconds break before the next attempt...")
                time.sleep(60*(times+1)) 
            else: 
                print(f"All {attempts} attempts failed. Please try again later.")
                if package_name is not None:
                    save_chat_history(history, package_name)
                raise e




def save_chat_history(history, package_name):
    curr_time = datetime.datetime.now()
    curr_time_string = curr_time.strftime("%Y-%m-%d %H-%M-%S")
    file_name = f"./chat_history/{package_name}_chat_{curr_time_string}.json"
    with open(file_name, 'w') as file:
        json.dump(history, file)

def get_model_name(response):
     model_name = response["model"]
     return model_name

def get_message(response):
    message = response["choices"][0]["message"]["content"]
    return message


