# Audio Handling Reference

> Audio duration estimation, voice parameters, inner OS, and dialogue relationship rules.

## Duration Estimation Formula

**Base speech rates:**

| Speech Type | Rate | Notes |
|-------------|------|-------|
| Normal | 4-5 chars/sec | Standard conversational speed |
| Low voice / Inner OS | 3-4 chars/sec | Contemplative, whispered |
| Loud / Urgent | 5-6 chars/sec | Shouting, panicked |

**Pause calculations:**
- Period `.` = 1 second
- Comma `,` = 0.5 second
- Ellipsis `...` = 1.5 seconds

**Formula:**
```
Duration (sec) = (Character count / Speech rate) + Sum of all pauses
```

## Audio Types

### Dialogue
- Format: `Character@: Content`
- Must be complete and un-split
- Calculate duration per line

### Inner OS (Internal Monologue)
- Format: `Character@InnerOS: Content`
- Duration equivalent to dialogue (do not compress)
- Annotate: `(mouth not moving)`
- Preserve original ellipsis `...`, do not complete
- After adding inner OS, must recalculate total shot duration

### Voiceover / Narration
- Treated same as dialogue for duration calculation
- Consider whether to replace with visual (Step 2d omission rules)

## Voice Parameter Template

For each audio line, add voice parameters:

```
Gender: [Male/Female]
Age: [Child/Young/Middle-aged/Elderly]
Tone: [High/Medium/Low]
Quality: [Clear/Hoarse/Warm/Cold]
Pronunciation: [Standard/Regional accent/ lisp/etc.]
Breath: [Steady/Heavy/Shallow/Rapid]
Volume: [Soft/Medium/Loud]
Speed: [Slow/Normal/Fast/Urgent]
```

**Example:**
```
Su Jin@ says: "Who dares touch my people?"
[Voice: Female, Young, Medium tone, Clear, Standard, Steady breath, Loud, Normal speed]
```

## Dialogue Relationship Rules (Seedance2.0)

### Position Establishment
- Always establish spatial relationship first: `A and B stand before XXX`
- Or: `A at XX position says: ...`
- Let video model determine whether to give reaction shots

### Reaction Shots
- Can insert reaction shots between dialogue segments
- Pattern: `A says: ...` -> `B happily looks at A` (reaction shot) -> `A continues: ...`
- Can split one audio segment, inserting reaction shots in between
- Audio integrity must be maintained

### Multi-Person Dialogue
- Clarify speaking target: `Su Jin says to Su Cheng: dialogue`
- Ensure model knows who is being addressed

## Audio Safety Checks

1. **Before splitting shots**: Calculate audio duration for each line
2. **After assigning audio**: Mentally mark each line in source script
3. **After all splitting**: Quick scan source script, confirm all quoted/colon-marked content assigned
4. **After adding inner OS**: Recalculate total shot duration
5. **Flag if any single audio >= 15s**: Warn user "Audio requires modification, exceeds shot duration limit"
