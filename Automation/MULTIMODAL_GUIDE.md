# Multimodal Bug Report Guide

## Overview
You can now include images in bug reports to help the LLM better understand the reproduction steps. This is especially useful for bugs that require:
- Opening external apps (browsers, etc.)
- Copying formatted content
- Multi-app interactions
- Visual verification of UI states

## Bug Report Format

### Text Format with Image Markers
Use the `[IMAGE:path/to/image.png]` marker to reference images in your bug report:

```
### STEPS TO REPRODUCE
[STEP 1] Open a web browser (e.g., Chrome Mobile)
[IMAGE:images/newpipe_5912_step1.png]

[STEP 2] Search for "HTML underline tag example"
[IMAGE:images/newpipe_5912_step2.png]

[STEP 3] Find and select formatted text (underlined, bold, etc.)
[IMAGE:images/newpipe_5912_step3.png]

[STEP 4] Copy the formatted text
[IMAGE:images/newpipe_5912_step4.png]

[STEP 5] Open NewPipe app
[IMAGE:images/newpipe_5912_step5.png]

[STEP 6] Paste into search bar
[IMAGE:images/newpipe_5912_step6.png]

[STEP 7] Observe the bug
[EXPECTED] Text should be plain
[ACTUAL] Formatting is preserved
[IMAGE:images/newpipe_5912_step7.png]
```

## Directory Structure
```
Automation/
  BRs/
    images/              # Create this folder
      newpipe_5912_step1.png
      newpipe_5912_step2.png
      ...
    NewPipe_v0.20.11_enhanced.txt  # Bug report with image markers
    NewPipe_v0.20.11.txt           # Old format still works
```

## Image Guidelines

### What to Capture
1. **Before state**: Screenshot showing the starting point
2. **Key actions**: Screenshots showing what to click/interact with
3. **Expected vs Actual**: Screenshots showing the bug manifestation

### Image Requirements
- Format: PNG or JPG
- Resolution: Device screenshot resolution (typically 1080x2340 or similar)
- Naming: Use descriptive names like `appname_issuenum_stepN.png`
- Location: Place in `Automation/BRs/images/` folder

### Taking Screenshots
You can capture screenshots from:
- Android emulator (Ctrl+S or screenshot button)
- Real device (adb shell screencap)
- Manual test runs

```bash
# Capture screenshot from emulator/device
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png images/newpipe_5912_step1.png
```

## Example: NewPipe HTML Formatting Bug

This bug requires:
1. Opening Chrome browser (external app)
2. Finding HTML formatted text
3. Copying the formatted content
4. Pasting into NewPipe

**Why images help:**
- Shows exactly what "HTML formatted text" looks like
- Demonstrates how to select and copy from browser
- Clarifies the expected vs actual behavior visually
- LLM can see UI elements to interact with

## Benefits

### For Complex Bugs
- **Multi-app workflows**: LLM sees which app to open
- **Visual context**: Shows what formatted text looks like
- **Clipboard content**: Demonstrates what to copy
- **UI identification**: Helps LLM find correct elements

### For Reproduction Success
- Reduces ambiguity in steps
- Shows exact UI state at each step
- Helps LLM understand context
- Improves action selection

## Backward Compatibility

Old format bug reports (text-only) still work:
- System detects format automatically
- No images = text-only mode
- With images = multimodal mode

## Installation

Install required dependencies:
```bash
source env/bin/activate
pip install -r requirements.txt
```

This will install Pillow (PIL) for image processing.

## Usage

Run reproduction with enhanced bug report:
```bash
python Automation/reproduction.py BRs/NewPipe_v0.20.11_enhanced.txt
```

Or use the regular text-only format:
```bash
python Automation/reproduction.py BRs/NewPipe_v0.20.11.txt
```

## Tips for Creating Effective Bug Reports

1. **One image per step**: Don't overload with too many images
2. **Highlight important areas**: Use annotations if needed
3. **Show state changes**: Before/after screenshots
4. **Include error states**: Screenshot when bug manifests
5. **Keep text clear**: Images supplement, don't replace text

## Troubleshooting

### Images not loading
- Check path is relative to BR file: `images/filename.png`
- Verify images exist in `Automation/BRs/images/`
- Check image format (PNG/JPG supported)

### Performance issues
- Limit to 5-8 images per bug report
- Resize large images if needed
- Compress images to reduce token usage

### LLM not understanding
- Add more descriptive text alongside images
- Highlight or annotate key UI elements
- Include both wide view and close-up shots
