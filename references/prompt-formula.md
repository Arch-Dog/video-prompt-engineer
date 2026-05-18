# Prompt Formula Reference

> 提示词撰写公式、格式规范与动作描述规则。

## Universal Formula

```
[Atmosphere] + [Timestamp: Action description (scene/position/face direction/gaze) + Audio content] + Cinematic sound effects, no music, no subtitles
```

**Transition markers** are post-editing decisions — do NOT write into prompt. Record in spatial scheduling document only.

## Component Rules

### Atmosphere
- Add 3-5 character atmosphere phrase at emotional turning points or scene transitions
- Not every shot needs it

### Scene
- Scene info naturally integrated through action description (e.g., "Su Mansion@red lanterns hanging in courtyard")
- First appearance in continuous same-scene shots: annotate scene@
- Subsequent shots: no repetition

### Timestamp Shot Breakdown

**Format:**
```
"Start sec~End sec, action description; Next segment start sec~End sec, action description..."
```

**Example:**
```
"0~5 sec, camera follows Yunmiao's back walking in rain, raindrops hitting oil-paper umbrella, Yunmiao@ says: Dialogue 1; 6~12 sec, camera slowly pushes in, Yunmiao stops and looks up ahead"
```

**Segment Rules:**
- Each segment 3-6 seconds, corresponding to one visual event
- Action turning point starts new segment
- Shot scale in natural language: "camera focuses on... close-up""camera slowly pushes in""camera pulls back"
- Timestamps rounded to integers, segments within same shot connect end-to-end

### Action Description Rules

**1. Visual-first priority — include:**
- Environmental interaction: "raindrops hitting oil-paper umbrella"
- Texture details: "vermillion Chinese-style gate"
- Dynamic elements: "several fallen leaves drifting down"
- Sound details: "creaking sound, gate pulled open from inside"
- Body details: "slender back""withered hand""corner of mouth slightly twitching"
- Serendipity: "a withered ginkgo leaf happens to fall on her palm"

**2. Subject + Position**: Every action description includes subject (character name) and position info

**3. Face Direction + Gaze**: Annotate for dialogue scenes or when character focus needs clarification (e.g., "face towards gate, gaze falling on door plaque"). Can omit for solo actions or environment descriptions

**4. Action Rhythm:**
- Fast actions: short sentences ("shoves open violently")
- Slow actions: slightly longer sentences + sufficient time

**5. Temporal Connectors:** "Then""afterwards""while... simultaneously..." etc. to connect actions

**6. State Transitions:** Mark emotional state changes ("extracting from sadness""restoring patriarchal dignity") so model understands emotional layers

**7. Character Blocking Consistency:** When same scene/same time period plot splits into multiple shots, each shot's prompt must contain identical character position relationship descriptions. Never omit because "previous shot already wrote it"

### Audio Content Annotation

**Format:**
- Dialogue: `Character@: Content` (The @ after character cannot be omitted, use colon before content, no quotation marks)
- Inner OS: `Character@InnerOS: OS content`. OS and dialogue completely equivalent in duration calculation, do not compress. Annotate "(mouth not moving)". Preserve original ellipsis "...", do not complete
- Voice color: Each audio adds voice parameters (gender/age/tone/quality/pronunciation/breath/volume/speed)

**Dialogue Relationships (Seedance2.0-based):**
- Establish position: `A and B stand before XXX`
- Can insert reaction shots: `A says: ...` -> `B happily looks at A` (reaction shot) -> `A continues: ...`
- Can split one audio segment, inserting reaction shots in between, maintaining audio integrity
- Multi-person dialogue: clarify speaking target (e.g., `Su Jin says to Su Cheng: dialogue`)

## Punctuation Standards

- Prompt wrapped in double quotes `"` (outer layer)
- No quotation marks inside dialogue, use colon to separate character and line
- Timestamp segments separated by semicolon `；`
- Example: `"0~5 sec, [Medium shot] Su Jin looks up in pit, Su Jin@ says: dialogue content; 6~10 sec, [Close-up] Su Cheng looks down clenching fist"`

## Object Description

- **Specific**: Write what script says (`two baskets vegetables and one basket ducks`), no abstract generalization (`vegetable-grain team`)
- **Shot independence**: No cross-shot references ("those vegetables""the thing just now") — describe anew each time

## Density Rules

- Information density moderate, 3-5s per visual event
- Single prompt <= 300 characters

## Unified Suffix

Every prompt ends with: `电影音效，无配乐，无字幕`

## Action Description Anti-Patterns

| Long/Complex Sentence | Split into Short Sentences |
|-----------------------|---------------------------|
| Push chair, stand up, walk to door, open door | Push chair -> Stand up -> Walk to door -> Open door |
| Turn to face Ning Hongfei, expression suddenly cold, point finger at betrothal gifts | Turn to face Ning Hongfei -> Expression suddenly cold -> Point finger at two baskets vegetables |
