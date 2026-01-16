#!/usr/bin/env python3
"""
Verify that images are being loaded from the NewPipe bug report
"""
import sys
sys.path.insert(0, '/Users/darshan/Desktop/Papers/ReBL/Automation')

from utils import read_bug_report
from PIL import Image
import os

# Test the NewPipe enhanced bug report
bug_report_path = "/Users/darshan/Desktop/Papers/ReBL/Automation/BRs/NewPipe_v0.20.11_enhanced.txt"

print("=" * 70)
print("VERIFYING IMAGE LOADING FOR NEWPIPE BUG REPORT")
print("=" * 70)

# Read the bug report
print(f"\n[1] Reading bug report: {os.path.basename(bug_report_path)}")
data = read_bug_report(bug_report_path)

# Check if it's the new format
if isinstance(data, dict):
    print("PASS: Bug report loaded in multimodal format (dict)")
    print(f"\n[2] Text content length: {len(data['text'])} characters")
    print(f"\n[3] Number of images found: {len(data['images'])}")
    
    if len(data['images']) > 0:
        print("\n[4] Image details:")
        for i, img_path in enumerate(data['images'], 1):
            print(f"\n   Image {i}:")
            print(f"   - Path: {img_path}")
            
            # Check if file exists
            if os.path.exists(img_path):
                print(f"   - Status: EXISTS")
                
                # Try to load the image
                try:
                    img = Image.open(img_path)
                    print(f"   - Size: {img.size}")
                    print(f"   - Format: {img.format}")
                    print(f"   - Mode: {img.mode}")
                    file_size = os.path.getsize(img_path)
                    print(f"   - File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
                    print(f"   - CAN BE LOADED BY PIL")
                except Exception as e:
                    print(f"   - ERROR LOADING: {e}")
            else:
                print(f"   - Status: NOT FOUND")
    else:
        print("\nWARNING: No images found in bug report!")
        print("   Check that [IMAGE:...] markers are present in the bug report")
else:
    print("FAIL: Bug report loaded in old text-only format")
    print("   The multimodal features are not being used!")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if isinstance(data, dict) and len(data['images']) > 0:
    print("PASS: Images WILL BE USED during bug reproduction")
    print("PASS: The LLM will receive both text and images")
    print("\nTo run reproduction with these images:")
    print("  python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11_enhanced.txt")
else:
    print("WARNING: Images NOT configured correctly")
    print("   Fix the bug report format or check image paths")

print()
