# Quality Rubric Reference

> 11-item quality checklist with priority levels and failure fallback rules.

## The 11 Checks

| ID | Check Item | Standard | Priority |
|----|-----------|----------|----------|
| D0 | Audio integrity | Every audio (dialogue/voiceover/inner OS) completely preserved, no splitting, no omission | **P0 Fatal** |
| D1 | Audio executability | Shot duration >= total audio content duration within shot, otherwise fail | **P0 Fatal** |
| D2/D3 | General checks | No time/perspective/emotion contradictions; no ambiguous descriptions | P2 General |
| D4 | Visual quality | Action descriptions include environmental interaction/texture details/dynamic elements; every sentence can be visualized | **P1 Serious** |
| D5 | Shot independence | Each shot independently executable, no cross-shot references ("those""just now") | **P1 Serious** |
| D6 | Information density | Density moderate, 3-5s per visual event, single prompt <= 300 chars | P2 General |
| D7 | Action description completeness | Subject + position + (when needed) face direction/gaze; same-scene continuous shots character blocking consistent | **P1 Serious** |
| D8 | Scene description preservation | Scene descriptions before characters enter must be preserved, cannot omit | P2 General |
| D10 | Shot merge verification | Verify Step 3 visual continuity: spatial consistency, eye direction match, no 180-degree violation, temporal continuity; same-scene continuous shots character blocking consistent | **P1 Serious** |
| D11 | Prompt spatial verification | Verify Step 4.5 output: do adjacent shots' Exit Frame and Entry Frame share visual anchor? Are spatial jumps recorded in spatial scheduling document with transition method? | **P1 Serious** |
| D12 | Audio quantity check | Total audio in script (dialogue + voiceover + OS) == total audio in shot table | **P1 Serious** |

## Notes

- Single audio (dialogue/voiceover/inner OS) >= 15s: flag with warning "Audio requires user modification, exceeds shot duration limit"
- After adding inner OS, must recalculate total shot duration

## Failure Fallback Rules

| Failure | Fallback Action |
|---------|-----------------|
| D12 fail (audio quantity mismatch) | Return to Step 3 to fill gaps |
| D0/D1 fail (audio issues) | Return to Step 3 to adjust shot splitting |
| D10 fail (shot merge issues) | Return to Step 3 to re-merge |
| D11 fail (prompt spatial description issues) | Return to Step 4 to modify prompt |
| Any step fails twice consecutively | Return to previous step to re-examine |

## Quick Self-Check (Step 4.5)

**Checklist:**
- Any abstract words like "very fast""very""suddenly""disappear" in prompt? -> Change to natural language description
- Is adjacent shot space traceable? -> Do previous shot ending and next shot beginning share visual elements?
- Are spatial jumps recorded in spatial scheduling document with transition method?

## Transition Methods Reference

Six options for spatial jumps (record only, do not write into prompt):

1. Action continues
2. Cut where she's looking
3. Sound arrives first
4. Same object connects
5. Light looks the same
6. Fade to black then light
