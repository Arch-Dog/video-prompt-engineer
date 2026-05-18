# Parser Guide

> Structured script parser for long scripts. Optional optimization for token efficiency.

## Purpose

Convert script text into structured JSON, avoiding repeated raw text reading in subsequent steps, saving tokens.

## When to Use

- Dialogue lines >= 20 OR scene count >= 5: recommended
- Dialogue lines >= 30 OR scene count >= 8: strongly recommended

## Usage

```bash
cd "/Users/cdx/.workbuddy/skills/video-prompt-engineer/scripts"
python3 parser.py script_temp.txt > structured_data.json
```

## Output Format

```json
{
  "characters": [
    {"name": "Character A", "count": 5, "has_ref_default": false},
    ...
  ],
  "scenes": [
    {"name": "Scene A", "count": 3, "has_ref": false, "has_ref_default": false},
    ...
  ],
  "dialogues": [
    {
      "content": "Dialogue content",
      "character": "Character A",
      "emotion": "Angry",
      "emotional_direction": "Angry",
      "speed_type": "normal",
      "duration": 8.5,
      "scene": "Scene A",
      "line_num": 12
    },
    ...
  ]
}
```

## Limitations

- Parser may not recognize all script formats
- If omissions found, manually supplement in subsequent steps
- This step is optional — short scripts can skip parser and proceed manually
