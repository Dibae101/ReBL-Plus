# Multimodal Bug Report Implementation - Summary

## What Was Done

I've implemented a multimodal bug report system that allows you to include images alongside text in your bug reports. This helps the LLM better understand complex reproduction steps, especially for bugs involving:
- Multi-app workflows (e.g., copy from Chrome, paste to NewPipe)
- Visual UI states
- Formatted content (HTML, rich text)
- External app interactions

## Changes Made

### 1. **Updated Core Files**

#### `Automation/utils.py`
- Modified `read_bug_report()` to return dict with text + image paths
- Extracts `[IMAGE:path]` markers from bug reports
- Converts relative paths to absolute paths
- Added `read_bug_report_simple()` for backward compatibility

#### `Automation/my_gpt.py`
- Added `from PIL import Image` import
- Created `convert_history_to_multimodal()` function
- Updated `generate_text()` to support multimodal mode
- Automatically detects if images are present in history
- Passes images to Gemini API alongside text

#### `Automation/reproduction.py`
- Updated `reproduce_bug()` to handle dict format from bug reports
- Adds images to conversation history
- Passes `use_multimodal=True` when images detected
- Backward compatible with old text-only format

#### `requirements.txt`
- Added `Pillow>=10.0.0` for image processing

### 2. **Created New Files**

#### Bug Reports
- `Automation/BRs/NewPipe_v0.20.11_enhanced.txt` - Enhanced version with image markers
- Original `NewPipe_v0.20.11.txt` still works (backward compatible)

#### Documentation
- `Automation/MULTIMODAL_GUIDE.md` - Complete guide for creating multimodal reports
- `Automation/BRs/NEWPIPE_5912_SETUP.md` - Specific guide for this bug

#### Utilities
- `test_multimodal.py` - Test script to verify setup
- `create_placeholder_images.py` - Generate placeholder images for testing

#### Images Directory
- `Automation/BRs/images/` - Contains 8 placeholder images for NewPipe bug

## How It Works

### Bug Report Format

Instead of plain text, use image markers:

```text
### STEPS TO REPRODUCE
[STEP 1] Open Chrome browser
[IMAGE:images/newpipe_5912_step1.png]

[STEP 2] Search for HTML examples
[IMAGE:images/newpipe_5912_step2.png]
```

### Image Processing Flow

1. **Bug report parsing**: `read_bug_report()` extracts text and finds all `[IMAGE:path]` markers
2. **Path resolution**: Converts relative paths to absolute based on bug report location
3. **Image loading**: PIL opens each image file
4. **Multimodal format**: Text and images combined into Gemini-compatible format
5. **API call**: Gemini receives both text context and visual information

### Gemini API Integration

```python
# History with images
history = [
    {
        "role": "user",
        "content": "Bug Report: ...",
        "images": ["/path/to/step1.png", "/path/to/step2.png"]
    }
]

# Converted to multimodal content
contents = [
    "User: Bug Report: ...",
    PIL.Image (step1.png),
    PIL.Image (step2.png)
]

# Sent to Gemini
response = model.generate_content(contents)
```

## Testing

### Run Tests
```bash
cd /Users/darshan/Desktop/Papers/ReBL
source env/bin/activate
python test_multimodal.py
```

### Results
✓ All 8 images created and loaded successfully
✓ Bug report parsing working correctly
✓ Backward compatibility maintained
✓ Ready for testing with reproduction script

## Usage

### Option 1: Test with Placeholders (Quick)
```bash
# Placeholders already created, just run:
source env/bin/activate
python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11_enhanced.txt
```

### Option 2: Use Real Screenshots (Recommended)
```bash
# 1. Start emulator
~/Library/Android/sdk/emulator/emulator -avd Pixel_4 &

# 2. Capture screenshots for each step
adb shell screencap -p /sdcard/step1.png
adb pull /sdcard/step1.png Automation/BRs/images/newpipe_5912_step1.png
# Repeat for steps 2-8

# 3. Run reproduction
python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11_enhanced.txt
```

### Option 3: Use Old Format (No Images)
```bash
# Original format still works
python Automation/reproduction.py Automation/BRs/NewPipe_v0.20.11.txt
```

## Why This Solves Your Problem

### The Issue
The LLM was failing because:
- It didn't understand "open a web browser" required opening Chrome
- It didn't know what "HTML formatted text" looks like visually
- It skipped the browser interaction entirely
- It pasted plain text from clipboard instead of formatted HTML text

### The Solution
With images, the LLM can now:
1. **See Chrome icon** → Understands to open browser app
2. **See formatted webpage** → Knows what to look for
3. **See text selection** → Understands copy action
4. **See search bar** → Knows where to paste
5. **See underlined text** → Can verify bug occurred

### Expected Improvement
- **Before**: Failed at "paste" step with wrong clipboard content
- **After**: Should successfully navigate Chrome → copy formatted text → paste to NewPipe → verify formatting

## Next Steps

### For Immediate Testing
1. ✅ System is ready to test with placeholders
2. Run reproduction script with enhanced bug report
3. Observe if LLM now understands to open Chrome
4. Check if it navigates to browser correctly

### For Production Use
1. Capture real screenshots from emulator (see `NEWPIPE_5912_SETUP.md`)
2. Replace placeholders with actual app screenshots
3. Optionally annotate images (arrows, highlights)
4. Re-run reproduction and compare results

### For Other Bugs
1. Follow format in `NewPipe_v0.20.11_enhanced.txt`
2. Use `[IMAGE:images/bugname_stepN.png]` markers
3. Place images in `Automation/BRs/images/`
4. Use descriptive filenames: `appname_issuenum_stepN.png`

## Benefits

### For Complex Bugs
- **Multi-app workflows**: Visual guidance for app switching
- **UI interactions**: Shows exactly which element to tap
- **Visual states**: Confirms correct screen is displayed
- **Content types**: Clarifies "formatted", "styled", "rich" text

### For Reproduction Success
- Reduces ambiguity in steps
- Provides visual confirmation points
- Helps LLM make better action decisions
- Easier to debug when reproduction fails

## Files Modified

```
Modified:
  Automation/utils.py
  Automation/my_gpt.py
  Automation/reproduction.py
  requirements.txt

Created:
  Automation/BRs/NewPipe_v0.20.11_enhanced.txt
  Automation/BRs/images/ (directory)
  Automation/BRs/images/newpipe_5912_step*.png (8 files)
  Automation/MULTIMODAL_GUIDE.md
  Automation/BRs/NEWPIPE_5912_SETUP.md
  test_multimodal.py
  create_placeholder_images.py
```

## Verification Checklist

- ✅ Pillow installed
- ✅ Image directory created
- ✅ 8 placeholder images generated
- ✅ Bug report parser works
- ✅ Multimodal conversion works
- ✅ Images load correctly
- ✅ Backward compatibility maintained
- ✅ Test script passes
- ⏳ Ready for reproduction test

## Troubleshooting

### If reproduction still fails:
1. Check console output - are images being loaded?
2. Verify Gemini API supports image inputs (it should)
3. Try adding more images for intermediate steps
4. Annotate images with arrows/highlights
5. Make step descriptions more detailed

### If images don't load:
1. Check paths are relative: `images/file.png` not `/absolute/path`
2. Verify images exist: `ls Automation/BRs/images/`
3. Check image format: PNG or JPG
4. Run test script: `python test_multimodal.py`

## Contact & Support

For issues or questions:
- Review guides: `MULTIMODAL_GUIDE.md`, `NEWPIPE_5912_SETUP.md`
- Run tests: `python test_multimodal.py`
- Check console output for image loading errors
- Verify Pillow: `pip show Pillow`

---

**Status**: ✅ Implementation complete and tested
**Next**: Run reproduction with enhanced bug report and compare results
