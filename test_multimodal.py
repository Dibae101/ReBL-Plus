#!/usr/bin/env python3
"""
Test script to verify multimodal bug report loading works correctly
"""
import sys
import os
sys.path.insert(0, '/Users/darshan/Desktop/Papers/ReBL/Automation')

from utils import read_bug_report
from PIL import Image

def test_bug_report_loading():
    """Test that bug reports load correctly with and without images"""
    
    print("=" * 60)
    print("Testing Multimodal Bug Report Loading")
    print("=" * 60)
    
    # Test 1: Enhanced bug report with images
    print("\n[Test 1] Loading enhanced bug report with images...")
    enhanced_report = "/Users/darshan/Desktop/Papers/ReBL/Automation/BRs/NewPipe_v0.20.11_enhanced.txt"
    
    try:
        data = read_bug_report(enhanced_report)
        
        if isinstance(data, dict):
            print("✓ Report loaded as dictionary (new format)")
            print(f"✓ Text length: {len(data['text'])} characters")
            print(f"✓ Images found: {len(data['images'])}")
            
            # Check each image
            for i, img_path in enumerate(data['images'], 1):
                if os.path.exists(img_path):
                    try:
                        img = Image.open(img_path)
                        print(f"  ✓ Image {i}: {os.path.basename(img_path)} - {img.size} - OK")
                    except Exception as e:
                        print(f"  ✗ Image {i}: {os.path.basename(img_path)} - Cannot open: {e}")
                else:
                    print(f"  ⚠ Image {i}: {img_path} - NOT FOUND (create placeholders or capture screenshots)")
        else:
            print("✗ Report loaded as string (old format) - expected dictionary")
    except Exception as e:
        print(f"✗ Error loading enhanced report: {e}")
    
    # Test 2: Original bug report (backward compatibility)
    print("\n[Test 2] Loading original bug report (text-only)...")
    original_report = "/Users/darshan/Desktop/Papers/ReBL/Automation/BRs/NewPipe_v0.20.11.txt"
    
    try:
        data = read_bug_report(original_report)
        
        if isinstance(data, dict):
            print("✓ Report loaded as dictionary")
            print(f"✓ Text length: {len(data['text'])} characters")
            print(f"✓ Images found: {len(data['images'])} (should be 0)")
        else:
            print("✗ Report loaded as string - expected dictionary format")
    except Exception as e:
        print(f"✗ Error loading original report: {e}")
    
    # Test 3: Check image directory
    print("\n[Test 3] Checking image directory...")
    image_dir = "/Users/darshan/Desktop/Papers/ReBL/Automation/BRs/images"
    
    if os.path.exists(image_dir):
        print(f"✓ Image directory exists: {image_dir}")
        images = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        print(f"✓ Images in directory: {len(images)}")
        for img in images:
            print(f"  - {img}")
    else:
        print(f"⚠ Image directory not found: {image_dir}")
        print("  Create it with: mkdir -p Automation/BRs/images")
    
    print("\n" + "=" * 60)
    print("Testing Complete")
    print("=" * 60)
    
    # Summary
    print("\n[Next Steps]")
    print("1. If images are missing, capture screenshots or create placeholders")
    print("2. See Automation/BRs/NEWPIPE_5912_SETUP.md for screenshot guide")
    print("3. Run: python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11_enhanced.txt")
    print()

if __name__ == "__main__":
    test_bug_report_loading()
