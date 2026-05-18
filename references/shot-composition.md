# Shot Composition Reference

> 镜头切分、合并与空间调度规则。

## Beat-to-Shot Mapping

**Beat** = the minimal unit where emotional direction changes.
**Shot** = the minimal physically executable unit.

- One beat != necessarily one shot (different granularity)
- Shot split points: scene change, dialogue completeness boundary, physically unmergeable actions
- Emotional turns can happen within a shot (via reaction shots, close-up switches)
- Merge priority: same scene + emotional coherence + no dialogue splitting

## Shot Splitting Rules

**Core Constraints:**
- **Audio integrity**: Complete audio (dialogue/voiceover/inner OS) cannot be split (can split before/after audio)
- **Audio duration rigidity**: Shot duration >= total audio duration within shot. Flag if single audio > 15s
- **Scene change = mandatory split**

**Split Criteria:**
1. Audio duration estimation (speech rate + pauses):
   - Normal speed: 4-5 chars/sec, period 1s, comma 0.5s
   - Low voice/inner OS: 3-4 chars/sec
   - Loud/urgent: 5-6 chars/sec
2. Speaking is an action — audio duration = this action's duration
3. After adding inner OS, must recalculate shot duration
4. **Audio omission prevention**: After splitting, mentally mark each audio in source script. Quick scan to confirm all quoted/colon-marked dialogue and OS are assigned

## Shot Merging Rules

**Target: 10-15 seconds per shot**

1. **Same scene priority**: Continuous shots within same scene without scene changes can merge
2. **Emotional coherence**: Shots without essential emotional direction change can merge
3. **No audio splitting**: Merging must not break audio integrity
4. **Duration ceiling**: Merged shot <= 15s (if audio total already near 15s, no more merging)
5. **Post-merge check**: Information density moderate, 3-5s per visual event, each shot independently executable

## Spatial Continuity Verification

After merging, verify:
- **Spatial consistency**: Character's left/right position in frame doesn't jump (unless plot requires)
- **Eye direction match**: If A looks at B, next shot B's gaze direction should echo A's shot
- **Action axis**: No 180-degree rule violation
- **Temporal continuity**: Action start/end frames naturally connect across adjacent shots

## Spatial Scheduling

**Reference-image scenes:**
- No spatial details set, model references images
- Spatial details determined by model from images

**Non-reference-image scenes:**
- Deduce from script, once determined, spatial relationships remain constant in subsequent shots

**Visual Coherence:**
- Each shot: 1 core subject + 1-2 secondary elements
- Adjacent shots connected through shot language
- **Spatial continuity pre-planning**: If spatial position jumps between adjacent shots, plan transition method in advance. Record in spatial scheduling document, NOT in prompt

## Transition Methods (6 Options)

Record in spatial scheduling document only. Do NOT write into prompt.

1. Action continues
2. Cut where she's looking
3. Sound arrives first
4. Same object connects
5. Light looks the same
6. Fade to black then light

## Shot Scale Guide

| Scale | Purpose | Use Case |
|-------|---------|----------|
| Wide shot | Establish environment, show full view | Scene opening, character entrance, breathing room |
| Medium shot | Show character half-body + environment | Dialogue, daily interaction, multi-person scenes |
| Close-up | Focus on face + expression | Emotional reaction, key dialogue |
| Extreme close-up | Extreme focus on detail | Object detail, emotional climax, key action |

**Scale-to-Emotion Mapping:**
- Dialogue/Daily: Medium shot
- Emotional turn: Medium -> Close-up
- Key dialogue/Reaction: Close-up
- Character entrance: Wide -> Medium
- Object/Detail emphasis: Extreme close-up
- Breathing room/Contemplation: Wide shot

## Why No Camera Movement in Prompts

- Short drama doesn't need complex camera work, simple and direct is best
- Overly precise camera constraints limit model performance
- More detailed action description = model better judges appropriate camera work
