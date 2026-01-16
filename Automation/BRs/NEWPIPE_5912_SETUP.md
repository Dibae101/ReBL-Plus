# NewPipe Bug #5912 - Multimodal Setup Guide

## Bug Overview
**Issue**: Text copied from HTML is rendered in search bar with formatting preserved

**Why Images Are Needed**: This bug requires copying formatted text from Chrome browser. The LLM needs to see:
1. What "HTML formatted text" looks like visually
2. How to open and interact with Chrome
3. How to select and copy the formatted content
4. The actual vs expected behavior in NewPipe

## Quick Start

### Option 1: Use Placeholder Images (Testing)
For initial testing, create placeholder images:

```bash
cd /Users/darshan/Desktop/Papers/ReBL/Automation/BRs

# Create simple placeholder images (requires ImageMagick)
for i in {1..8}; do
  convert -size 1080x2340 xc:white -pointsize 48 -fill black \
    -gravity center -annotate +0+0 "Step $i" \
    images/newpipe_5912_step${i}.png
done
```

Or manually create 8 blank PNG files named `newpipe_5912_step1.png` through `newpipe_5912_step8.png`

### Option 2: Capture Real Screenshots

#### Step 1: Start Emulator & Open Chrome
```bash
# Ensure emulator is running
~/Library/Android/sdk/emulator/emulator -avd Pixel_4 &

# Wait for boot, then capture home screen
adb shell screencap -p /sdcard/step1.png
adb pull /sdcard/step1.png images/newpipe_5912_step1.png
```

#### Step 2: Search for HTML Examples
```bash
# Open Chrome and search "HTML underline tag example"
adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main

# Manually navigate and search, then capture
adb shell screencap -p /sdcard/step2.png
adb pull /sdcard/step2.png images/newpipe_5912_step2.png
```

#### Step 3: Show Formatted Text
```bash
# Navigate to a page with underlined/formatted text
# Example: https://www.w3schools.com/tags/tag_u.asp
# Capture the page showing formatted text
adb shell screencap -p /sdcard/step3.png
adb pull /sdcard/step3.png images/newpipe_5912_step3.png
```

#### Step 4: Text Selection
```bash
# Long-press on formatted text to select
# Capture with selection handles visible
adb shell screencap -p /sdcard/step4.png
adb pull /sdcard/step4.png images/newpipe_5912_step4.png
```

#### Step 5: Open NewPipe
```bash
# Go back to home and open NewPipe
adb shell am start -n org.schabi.newpipe/.MainActivity

adb shell screencap -p /sdcard/step5.png
adb pull /sdcard/step5.png images/newpipe_5912_step5.png
```

#### Step 6: Tap Search Bar
```bash
# Tap on search icon/bar in NewPipe
# Capture with search bar focused
adb shell screencap -p /sdcard/step6.png
adb pull /sdcard/step6.png images/newpipe_5912_step6.png
```

#### Step 7: Paste
```bash
# Long press in search bar and tap paste
# Capture the paste menu
adb shell screencap -p /sdcard/step7.png
adb pull /sdcard/step7.png images/newpipe_5912_step7.png
```

#### Step 8: Bug Manifestation
```bash
# Capture search bar showing UNDERLINED text (the bug)
# This should show formatting preserved in NewPipe
adb shell screencap -p /sdcard/step8.png
adb pull /sdcard/step8.png images/newpipe_5912_step8.png
```

## Annotating Screenshots (Optional but Recommended)

Use any image editor to add annotations:
- Red arrows pointing to key UI elements
- Red boxes highlighting the formatted text
- Text labels explaining what to look for

Example tools:
- Preview (Mac): Tools > Annotate
- GIMP (cross-platform)
- Any online image editor

## Running the Test

Once images are in place:

```bash
cd /Users/darshan/Desktop/Papers/ReBL

# Activate environment
source env/bin/activate

# Run with enhanced bug report
python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11_enhanced.txt
```

## Expected Improvements

### Without Images (Current Behavior)
- LLM doesn't understand "open browser"
- Skips Chrome interaction
- Pastes whatever is in clipboard
- Fails to reproduce bug

### With Images (Expected Behavior)
- LLM sees Chrome icon and understands to open it
- Recognizes formatted text on webpage
- Understands selection and copy action
- Correctly pastes into NewPipe
- Validates formatting is preserved

## Verification

Check that images are loaded correctly:

```python
from PIL import Image
import os

image_dir = "Automation/BRs/images"
for i in range(1, 9):
    img_path = f"{image_dir}/newpipe_5912_step{i}.png"
    if os.path.exists(img_path):
        img = Image.open(img_path)
        print(f"Step {i}: {img.size} - OK")
    else:
        print(f"Step {i}: MISSING!")
```

## Troubleshooting

### "No such file" error
- Ensure images directory exists: `mkdir -p Automation/BRs/images`
- Check image paths in bug report match actual files
- Use relative paths: `images/filename.png`, not absolute paths

### Images not helping
- Make sure images show clear UI states
- Add more descriptive text alongside images
- Annotate images to highlight key areas
- Consider adding intermediate steps

### Still failing reproduction
- Check that Chrome is installed on emulator
- Verify NewPipe APK is installed (v0.20.11)
- Ensure clipboard has formatted text, not plain text
- Review LLM output to see which step fails

## Alternative: Use Existing Screenshots

If you have screenshots from the original GitHub issue, you can use those:
1. Download images from GitHub issue #5912
2. Rename to match the naming convention
3. Place in `Automation/BRs/images/`
4. Update bug report with correct filenames

## Next Steps

1. Create/capture the 8 screenshots
2. Place them in `Automation/BRs/images/`
3. Run the enhanced bug report
4. Compare results with non-image version
5. Iterate on image quality/annotations if needed

## Contact & Support

If you encounter issues:
- Check image file permissions
- Verify Pillow installation: `pip show Pillow`
- Test with simple bug report first
- Review console output for image loading errors
