# OpenClaw Feishu Card Customization Reference

This reference captures a proven debugging and implementation approach for OpenClaw Feishu card customization, especially when the desired UX includes:

- card 2.0 containerized layouts
- streaming answers
- raw reasoning visibility
- collapsible reasoning panels
- unified titles/colors across all message paths

## 1. The most important lesson

When a Feishu card regression appears, do not start by tweaking the visual template.

First determine which of these is broken:
- provider did not emit readable live reasoning
- current session lost reasoning state
- runtime callback wiring is wrong
- card streaming lane logic is wrong
- Feishu send/reply/update API path failed

Visual symptoms often come from lower layers.

## 2. Proven root-cause patterns

### Pattern A: Only shows `Thinking...`

Possible causes:
- no live reasoning events exist
- session lost `reasoningLevel=stream`
- `onReasoningStream` is attached to the wrong layer

What to check:
- current session file
- raw stream log
- runtime logs for `onReasoningStream`

### Pattern B: Raw reasoning repeats itself

Possible causes:
- runtime emits cumulative snapshots
- wrapper text like `Reasoning:` and outer italics are not normalized
- async queue uses mutable shared text and replays later content

Fix strategy:
- normalize snapshot
- compute delta against prior snapshot
- freeze queued text before async update

### Pattern C: Final answer exists but user cannot see it

Possible causes:
- final answer is suppressed by commentary filters
- streaming close/update failure prevents fallback send
- reply API path fails while direct send path would work

Fix strategy:
- confirm final answer exists in session transcript
- inspect reply/send API failures
- add fallback from reply to direct send where appropriate

### Pattern D: Works until a new session starts

Possible causes:
- session init does not preserve reasoning state
- only current session entry was patched manually

Fix strategy:
- patch session initialization defaults for the intended Feishu scope

## 3. Card 2.0 structure that works well

Recommended high-level structure:

- card header
- reasoning `collapsible_panel`
  - element id for reasoning content
- answer content element

Reasoning panel states:
- expanded while raw reasoning streams
- collapsed once answer streaming begins

Header and template strategy:
- use one shared title/template selection path
- do not let fallback sends use a different legacy title

## 4. Runtime conditions that matter

For raw reasoning to actually appear, these conditions must all be true:

- the model/provider path emits readable live reasoning
- the current session is in reasoning stream mode
- the Feishu dispatcher is wired to actual runtime reply options
- the card has a visible reasoning lane

If any one of these is false, the front-end card cannot compensate.

## 5. Model/provider caveat

Different providers can expose reasoning differently:
- some provide readable live reasoning text
- some only provide final transcript thinking
- some provide encrypted reasoning blobs

Do not assume one successful provider path generalizes to another.

### Practical capability test

When checking a model for Feishu raw reasoning support, use this decision tree:

1. Verify the current session truly ran on the intended provider/model.
2. Check `raw-stream.jsonl`.
   - If it shows live thinking text events, the model/runtime can support true raw reasoning.
3. Check the saved session transcript.
   - If transcript has readable `thinking` but no live events, the model supports post-hoc thinking but not true live raw reasoning through the current runtime path.
4. If transcript has only encrypted/opaque reasoning payloads, treat it as non-displayable raw reasoning.

This prevents a common mistake:
- blaming Feishu card code for a model/provider capability limit.

## 5.1 Turn technical diagnosis into user choices

When capability limits are found, do not stop at the technical conclusion.

Translate them into practical options:

- `Current model cannot expose raw reasoning, but we can still improve card 2.0 styling.`
- `Current model cannot expose raw reasoning. If you want raw reasoning, we should switch models.`
- `Current model path is unstable. We should first fix session/provider routing, then continue with card customization.`

This makes the skill usable by non-expert users.

## 6. Persistence caveat

If the behavior works only until restart or only in one current session, the fix is incomplete.

A stable solution must survive:
- gateway restart
- new direct Feishu session
- normal fallback send paths

## 6.1 Restart policy

Do not silently restart `openclaw-gateway`.

Even if restart is technically necessary, the agent should:
- explain why restart is needed
- ask the user to run it or confirm permission first

Unexpected restarts can disrupt:
- active Feishu chats
- session-specific reasoning state
- ongoing tasks

## 7. Practical file map

Most work lands in:
- `extensions/feishu/src/reply-dispatcher.ts`
- `extensions/feishu/src/streaming-card.ts`
- `extensions/feishu/src/send.ts`
- `extensions/feishu/src/outbound.ts`
- `extensions/feishu/src/channel.ts`
- `extensions/feishu/src/config-schema.ts`

If symptoms and source do not match, inspect the actual runtime-loaded code path, which may be compiled `dist/`.
