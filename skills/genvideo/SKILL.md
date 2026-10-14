---
name: genvideo
description: Stage 4. Last resort after broll-select has searched the free stock libraries and found nothing - generate a short AI video clip. Asks before spending any credits.
---
# genvideo (stage 4)

**In plain words:** when no real footage exists (say, "a robot editing a film"), make a few seconds of it with an AI video tool.

## Steps
1. Take the `generated` rows from the asset plan, plus any b-roll rows broll-select could not fill from free stock. If broll-select has not searched yet, run it first.
2. Write one prompt per clip: subject, action, camera move, lighting, aspect ratio, length (3 to 5 s).
3. Tell the creator the tool, the number of clips and the cost. Wait for yes.
4. Generate, watch the result frame by frame, save to `assets/gen/`.

## Rules
- Never spend credits without a yes for that batch.
- Never generate a real person's likeness or a real brand's product.
- Reject clips with warped hands, melting text or flicker; regenerate once, then fall back to a card.
- Generated clips are support only. Never use one as proof of a claim.
