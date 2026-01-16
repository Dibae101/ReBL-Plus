
import re
import os
import ast
import json
from handle_command import *
import pandas as pd
from openpyxl import load_workbook
import subprocess
import base64

def clear_logcat(device_port):
    adb_command = ['adb', '-s', f'emulator-{device_port}', 'logcat', '-c']
    subprocess.run(adb_command)
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')





def get_logcat(device_port):
    #start_time = start_time.strftime('%m-%d %H:%M:%S.%f')[:-3]
    adb_command = ['adb', '-s', f'emulator-{device_port}', 'logcat', '-d', '*:E']
    try:
        result = subprocess.run(adb_command, capture_output=True, text=True,  timeout=2)
    except subprocess.TimeoutExpired:
        print("Get logcat did not complete within the timeout period.")
        return ''
    if result.returncode != 0:  # If the command wasn't successful
        raise Exception("adb logcat failed, make sure your device is connected and adb is installed")
    return result.stdout  # This is the output of the adb logcat command

def read_bug_report(file_path):
    """Read bug report and extract images if referenced"""
    with open(file_path, "r") as file:
        content = file.read()
    
    # Extract image paths
    import re
    image_pattern = r'\[IMAGE:(.*?)\]'
    image_paths = re.findall(image_pattern, content)
    
    # Return both text and image paths
    bug_report_text = re.sub(image_pattern, '', content)  # Remove image markers from text
    bug_report_text = ' '.join([line.strip() for line in bug_report_text.split('\n')])
    
    # Make image paths absolute
    base_dir = os.path.dirname(file_path)
    absolute_image_paths = [os.path.join(base_dir, img_path) for img_path in image_paths]
    
    return {
        'text': f"Bug Report: {bug_report_text}",
        'images': absolute_image_paths
    }

def read_bug_report_simple(file_path):
    """Simple version without multimodal support (backward compatible)"""
    with open(file_path, "r") as file:
        content = file.readlines()
    bug_report = ' '.join([line.strip() for line in content])
    return f"App Name: {file_path[11:file_path.find('_issue')]}. Bug Report: {bug_report}"

def load_training_prompts(path): 
    with open(path, 'r') as f:
        return json.load(f)
    
def convert_message_to_command_list(message):

    try: 
        if "[" in message and "]" in message:
            start_index = message.index("[")
            end_index = message.rindex("]")
            message = message[start_index:end_index+1]
            if message == "[]" or message == "[{}]":
                command_list = []
            else:
                command_list = ast.literal_eval(message)
        elif "{" in message and "}" in message:
            start_index = message.index("{")
            end_index = message.rindex("}")
            message = message[start_index:end_index+1]
            if message == "{}":
                command_list = []
            else:
                command_list = [ast.literal_eval(message)] 
        else:
            command_list = []
        return command_list
    except (ValueError, SyntaxError) as e:
        print(f"Unable to convert message to command list: {str(e)}")
        return []

def add_commands(commands, new_commands):
    if new_commands is None:
        return None
    commands.extend(new_commands)
    sequence = has_repeating_sequence(commands)
    if sequence: 
        return f"Repeating sequence detected: , {sequence}"
    return None

def has_repeating_sequence(commands):
    length = len(commands)
    for seq_length in range(1, length // 2 + 1):
        sequence = commands[length - 2*seq_length : length - seq_length]
        next_sequence = commands[length - seq_length:]
        if sequence == next_sequence:
            return sequence
    return None

def count_command_and_response(execution_data, command_list):
    execution_data[1] += 1
    execution_data[2] += len(command_list)