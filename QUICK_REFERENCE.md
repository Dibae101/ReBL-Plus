# Quick Reference: Multimodal Bug Reports

## Quick Start (3 Steps)

### 1. Test Current Setup
```bash
cd /Users/darshan/Desktop/Papers/ReBL
source env/bin/activate
python test_multimodal.py
```

### 2. Run with Placeholder Images
```bash
python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11_enhanced.txt
```

### 3. Compare with Text-Only Version
```bash
python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11.txt
```

## Creating Your Own Multimodal Bug Report

### Format Template
```text
App Name: YourApp

### STEPS TO REPRODUCE
[STEP 1] Description of first step
[IMAGE:images/yourapp_issue_step1.png]

[STEP 2] Description of second step
[IMAGE:images/yourapp_issue_step2.png]

[STEP 3] Expected vs Actual
[EXPECTED] What should happen
[ACTUAL] What actually happens (the bug)
[IMAGE:images/yourapp_issue_step3.png]
```

### Image Naming Convention
```
images/appname_issuenum_stepN.png

Examples:
  images/newpipe_5912_step1.png
  images/focus_4583_step1.png
  images/ankidroid_7070_step1.png
```

## Capturing Screenshots

### From Emulator
```bash
# Capture
adb shell screencap -p /sdcard/screenshot.png

# Pull to your computer
adb pull /sdcard/screenshot.png Automation/BRs/images/appname_issue_step1.png
```

### From Device
```bash
# Capture (device-specific, usually Power + Volume Down)
# Then pull
adb pull /sdcard/DCIM/Screenshots/screenshot.png Automation/BRs/images/appname_issue_step1.png
```

## File Structure
```
Automation/
  BRs/
    images/              ← Put images here
      newpipe_5912_step1.png
      newpipe_5912_step2.png
      ...
    NewPipe_v0.20.11_enhanced.txt    ← Bug report with [IMAGE:...] markers
    NewPipe_v0.20.11.txt              ← Original (still works)
```

## When to Use Images

✅ **Use images when:**
- Bug involves multiple apps (browser + app)
- Need to copy/paste formatted content
- Visual UI state is important
- Steps are ambiguous without seeing them
- External app interaction required

❌ **Don't need images when:**
- Simple single-app bug
- Steps are clear from text alone
- No visual ambiguity

## Troubleshooting

### Images not found
```bash
# Check they exist
ls Automation/BRs/images/

# Check paths in bug report match filenames
grep IMAGE: Automation/BRs/YourBugReport.txt
```

### Test not passing
```bash
# Run test
python test_multimodal.py

# Should show:
#   ✓ Images found: 8
#   ✓ Image 1: ... - OK
```

### Reproduction fails
1. Check console for image loading errors
2. Verify images show clear UI states
3. Add more descriptive text alongside images
4. Consider annotating images with arrows

## Documentation Files

- `MULTIMODAL_IMPLEMENTATION.md` - Complete implementation summary
- `Automation/MULTIMODAL_GUIDE.md` - Detailed usage guide
- `Automation/BRs/NEWPIPE_5912_SETUP.md` - NewPipe specific guide
- This file - Quick reference

## Testing Commands

```bash
# Activate environment
source env/bin/activate

# Test setup
python test_multimodal.py

# Create placeholders (if needed)
python create_placeholder_images.py

# Run reproduction (multimodal)
python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11_enhanced.txt

# Run reproduction (text-only)
python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11.txt
```

## Key Code Changes

### Bug Report Returns Dict Now
```python
# Old format (still works)
bug_report = read_bug_report("file.txt")
# Returns: string

# New format (with images)
bug_report_data = read_bug_report("file_enhanced.txt")
# Returns: {
#   'text': "Bug Report: ...",
#   'images': ['/path/to/img1.png', '/path/to/img2.png']
# }
```

### History Includes Images
```python
history.append({
    "role": "user",
    "content": "Bug Report text...",
    "images": [list of image paths]
})
```

### Gemini Receives Multimodal Content
```python
# Automatically handles text + images
response = generate_text(prompt, history, use_multimodal=True)
```

## What Changed for NewPipe Bug

### Before (Text Only)
```
STEPS TO REPRODUCE
1. Open a web browser
2. Copy formatted text
3. Paste to NewPipe
```
❌ LLM didn't understand "open browser" → Failed

### After (With Images)
```
[STEP 1] Open Chrome browser
[IMAGE:images/newpipe_5912_step1.png]  ← Shows Chrome icon

[STEP 2] Find formatted text
[IMAGE:images/newpipe_5912_step2.png]  ← Shows underlined text

[STEP 3] Copy the text
[IMAGE:images/newpipe_5912_step3.png]  ← Shows selection menu
```
✅ LLM sees visuals → Better understanding → Should work

## Success Criteria

After running enhanced reproduction, you should see:
- LLM opens Chrome (not skipped)
- LLM searches for HTML examples
- LLM copies formatted text (not plain text)
- LLM pastes to NewPipe
- LLM verifies formatting preserved (bug reproduced)

## Need Help?

1. Read `MULTIMODAL_IMPLEMENTATION.md` for full details
2. Run `python test_multimodal.py` to check setup
3. Check console output for specific errors
4. Verify images load: `python -c "from PIL import Image; Image.open('path/to/image.png').show()"`
