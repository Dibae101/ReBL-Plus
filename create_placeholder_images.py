#!/usr/bin/env python3
"""
Create placeholder images for NewPipe bug report testing
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(step_num, description, filename):
    """Create a simple placeholder image with text"""
    # Android phone typical resolution
    img = Image.new('RGB', (1080, 2340), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a larger font, fallback to default if not available
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        font_desc = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font_title = ImageFont.load_default()
        font_desc = ImageFont.load_default()
    
    # Draw step number
    title = f"Step {step_num}"
    draw.text((540, 800), title, fill='black', font=font_title, anchor='mm')
    
    # Draw description (word wrap)
    words = description.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=font_desc)
        if bbox[2] - bbox[0] > 900:  # Max width
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(test_line)
                current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw description lines
    y = 1000
    for line in lines:
        draw.text((540, y), line, fill='#666666', font=font_desc, anchor='mm')
        y += 60
    
    # Save image
    img.save(filename)
    print(f"Created: {filename}")

def main():
    """Create all placeholder images"""
    output_dir = "/Users/darshan/Desktop/Papers/ReBL/Automation/BRs/images"
    os.makedirs(output_dir, exist_ok=True)
    
    steps = [
        (1, "Open Chrome Browser", "Chrome icon visible on screen"),
        (2, "Search for 'HTML underline tag example'", "Search results showing HTML tutorial pages"),
        (3, "Find formatted text on webpage", "Page showing underlined and styled text"),
        (4, "Select and copy the formatted text", "Text selection with copy menu visible"),
        (5, "Open NewPipe app", "NewPipe main screen"),
        (6, "Tap on search bar", "Search bar activated with keyboard"),
        (7, "Long press and paste copied text", "Paste menu showing"),
        (8, "BUG: Formatting preserved in search bar", "Underlined text visible in search field"),
    ]
    
    for step_num, title, description in steps:
        filename = os.path.join(output_dir, f"newpipe_5912_step{step_num}.png")
        create_placeholder_image(step_num, f"{title}\n{description}", filename)
    
    print(f"\n✓ Created {len(steps)} placeholder images in {output_dir}")
    print("\nThese are simple placeholders. For better results:")
    print("1. Replace with real screenshots from emulator")
    print("2. Follow guide in Automation/BRs/NEWPIPE_5912_SETUP.md")
    print("\nYou can now test with:")
    print("  python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11_enhanced.txt")

if __name__ == "__main__":
    main()
