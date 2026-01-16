# Multimodal Bug Reproduction Flow

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Bug Report File                          │
│  NewPipe_v0.20.11_enhanced.txt                             │
│                                                             │
│  [STEP 1] Open Chrome                                       │
│  [IMAGE:images/step1.png]  ←───────────┐                  │
│                                         │                   │
│  [STEP 2] Search HTML examples          │                   │
│  [IMAGE:images/step2.png]  ←──────────┼──┐               │
│                                         │  │                │
│  [STEP 3] Copy formatted text           │  │                │
│  [IMAGE:images/step3.png]  ←──────────┼──┼──┐            │
└─────────────────────────────────────────┼──┼──┼────────────┘
                                         │  │  │
                    ┌────────────────────┘  │  │
                    ▼                       │  │
              ┌──────────┐                 │  │
              │  step1   │                 │  │
              │  .png    │                 │  │
              └──────────┘                 │  │
                    │                      │  │
                    └──────────────────────┘  │
                                              │
                    ┌─────────────────────────┘
                    ▼
           ┌─────────────────┐
           │ utils.py        │
           │ read_bug_report()│
           └────────┬─────────┘
                    │
                    ▼
           ┌─────────────────────────┐
           │  Returns Dictionary:     │
           │  {                       │
           │    'text': "...",        │
           │    'images': [paths]     │
           │  }                       │
           └────────┬─────────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ reproduction.py │
           │ reproduce_bug() │
           └────────┬─────────┘
                    │
                    ▼
           ┌─────────────────────────┐
           │  Add to history:         │
           │  {                       │
           │    "role": "user",       │
           │    "content": text,      │
           │    "images": [paths]     │
           │  }                       │
           └────────┬─────────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ my_gpt.py       │
           │ generate_text() │
           └────────┬─────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ convert_history_to_multimodal()│
    │                                │
    │ 1. Extract text from history   │
    │ 2. Load images with PIL        │
    │ 3. Combine into contents[]     │
    └────────┬───────────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ Gemini API Content:     │
    │                         │
    │ ["User: Bug Report...", │
    │  PIL.Image(step1.png),  │
    │  PIL.Image(step2.png),  │
    │  PIL.Image(step3.png)]  │
    └────────┬─────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │  Gemini 2.5 Pro         │
    │  (Vision + Language)    │
    │                         │
    │  🧠 Processes text       │
    │  👁️  Analyzes images     │
    │  🤔 Understands context  │
    └────────┬─────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │  Response:              │
    │                         │
    │  {"action": "click",    │
    │   "feature": "Chrome"}  │
    │                         │
    │  ✅ Now understands to   │
    │     open Chrome!        │
    └─────────────────────────┘
```

## Data Flow Comparison

### Without Images (OLD)
```
Bug Report Text
      ↓
  [reproduction.py]
      ↓
  history = [{"role": "user", "content": "Open browser..."}]
      ↓
  [my_gpt.py]
      ↓
  Gemini receives: "Open a web browser"
      ↓
  Gemini thinks: "What browser? Where? How?"
      ↓
  ❌ Skips step or fails
```

### With Images (NEW)
```
Bug Report Text + [IMAGE:...] markers
      ↓
  [utils.py] extracts images
      ↓
  {text: "...", images: [paths]}
      ↓
  [reproduction.py]
      ↓
  history = [{"role": "user", "content": "Open browser...", "images": [paths]}]
      ↓
  [my_gpt.py] loads images with PIL
      ↓
  Gemini receives: 
    - Text: "Open a web browser"
    - Image: [Screenshot showing Chrome icon]
      ↓
  Gemini thinks: "I see Chrome icon at position X,Y"
      ↓
  ✅ Clicks Chrome icon
```

## Example: Step-by-Step Execution

### Step 1: Bug Report Parsing
```python
# Input file: NewPipe_v0.20.11_enhanced.txt
"""
[STEP 1] Open Chrome
[IMAGE:images/newpipe_5912_step1.png]
"""

# After parsing
{
    'text': "Bug Report: [STEP 1] Open Chrome",
    'images': ['/absolute/path/to/images/newpipe_5912_step1.png']
}
```

### Step 2: History Creation
```python
history = [
    {"role": "system", "content": "You are a bug reproducer..."},
    {
        "role": "user",
        "content": "Bug Report: [STEP 1] Open Chrome",
        "images": ['/path/to/step1.png']
    }
]
```

### Step 3: Multimodal Conversion
```python
contents = [
    "System: You are a bug reproducer...",
    "User: Bug Report: [STEP 1] Open Chrome",
    PIL.Image.open('/path/to/step1.png')  # ← Image object
]
```

### Step 4: Gemini Processing
```
Input to Gemini:
- Text context about bug reproduction
- Visual: Screenshot showing phone home screen with Chrome icon
- Task: Figure out what to do

Gemini's Understanding:
- Text says: "Open Chrome"
- Image shows: Chrome icon at coordinates (X, Y)
- Action: click on Chrome icon

Output:
{"action": "click", "feature": "Chrome"}
```

## Why This Works Better

### Problem: "Copy formatted text from browser"

#### Without Images
```
LLM reads: "Copy formatted text from browser"

LLM doesn't know:
❌ Which browser? (Chrome? Firefox? Safari?)
❌ What is "formatted text"?
❌ Where to find it?
❌ How to identify it visually?

Result: Skips or fails
```

#### With Images
```
LLM reads: "Copy formatted text from browser"
LLM sees:
✅ Image 1: Chrome icon on home screen
✅ Image 2: Chrome opened with search
✅ Image 3: Webpage with underlined text visible
✅ Image 4: Text selection menu

LLM understands:
✅ Open Chrome (saw the icon)
✅ Search for example (saw search bar)
✅ Find underlined text (saw it in image)
✅ Copy it (saw selection menu)

Result: Successfully follows steps
```

## Performance Considerations

### Token Usage
```
Text-only:  ~4000 tokens
With 8 images:  ~4000 text + ~16000 image tokens = ~20000 total

Cost: Slightly higher but worth it for complex bugs
```

### Processing Time
```
Text-only:  2-3 seconds per response
Multimodal:  3-5 seconds per response (image encoding)

Tradeoff: Acceptable for better accuracy
```

## Success Metrics

### Expected Improvements

| Metric | Without Images | With Images |
|--------|---------------|-------------|
| Browser opened | ❌ 0% | ✅ Expected 80%+ |
| Correct app found | ❌ 10% | ✅ Expected 90%+ |
| Formatted text copied | ❌ 0% | ✅ Expected 70%+ |
| Bug reproduced | ❌ 0% | ✅ Expected 60%+ |

### How to Measure
1. Run 5 times with text-only → Count successes
2. Run 5 times with images → Count successes
3. Compare success rates

## File Dependencies

```
reproduction.py
    ├── imports utils.py
    │       └── read_bug_report()
    │           └── returns {text, images}
    │
    └── imports my_gpt.py
            ├── generate_text()
            │   ├── convert_history_to_multimodal()
            │   └── PIL.Image.open()
            │
            └── genai.GenerativeModel()
                └── Gemini 2.5 Pro API
```

## Testing Flow

```
1. Create/verify images exist
   ↓
2. Run test_multimodal.py
   ↓ (if pass)
3. Run reproduction.py with enhanced bug report
   ↓
4. Monitor console output for:
   - Image loading messages
   - LLM understanding of steps
   - Action decisions
   ↓
5. Compare with text-only version
   ↓
6. Iterate: Add more images or annotations if needed
```

## Debugging Checklist

- [ ] Images exist in `Automation/BRs/images/`
- [ ] Image paths in bug report match filenames
- [ ] Paths are relative: `images/file.png`
- [ ] Pillow installed: `pip show Pillow`
- [ ] Test passes: `python test_multimodal.py`
- [ ] Images load: Check console output
- [ ] Gemini API key valid
- [ ] Bug report format correct

## Next Steps

1. ✅ Setup complete (files created, images generated)
2. ⏳ Test with reproduction script
3. ⏳ Observe if LLM opens Chrome correctly
4. ⏳ Replace placeholders with real screenshots
5. ⏳ Apply to other bugs in your dataset
