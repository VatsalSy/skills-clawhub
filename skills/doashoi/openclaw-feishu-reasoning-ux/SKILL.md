---
name: openclaw-feishu-reasoning-ux
description: Improve OpenClaw's Feishu reply experience by customizing streaming cards, raw reasoning visibility, card 2.0 layouts, collapsible panels, titles, colors, and fallback send paths. Use this whenever a user wants a better Feishu reply UX for OpenClaw, especially when raw reasoning disappeared, only Thinking shows, titles/styles regressed, cards feel too black-box, or the user wants Feishu replies to become more observable, layered, and customizable.
---

# OpenClaw Feishu Reasoning UX

Use this skill when the task is specifically about how OpenClaw messages appear inside Feishu.

This skill is for:
- card 2.0 styling
- streaming card behavior
- raw reasoning visibility
- collapsible reasoning panels
- title/template/color behavior
- fallback send paths
- regressions after restart, update, or session rollover

This skill is not for generic Feishu app setup, permissions, or bot connectivity unless those directly block card delivery.

## Interaction style for end users

Assume many users do not know Feishu card internals, provider runtime details, or OpenClaw file layout.

So when using this skill:
- explain findings in plain language first
- translate technical diagnosis into user-facing choices
- proactively offer the next reasonable options instead of stopping at analysis
- ask short, concrete preference questions when appearance or behavior depends on taste

Good examples:
- `我检测到当前模型不支持可见 raw reasoning，但我们还能把回复卡片做成 2.0 风格、带颜色标题和折叠面板。你想先改这个吗？`
- `我检测到现在标题已经能改。你想让标题显示什么文案？直接告诉我文字就行。`
- `当前模型只能流正式回答，不能流 raw 思考。我可以帮你切到支持的模型，或者保留当前模型只优化卡片样式。你想走哪条？`

Do not dump only low-level findings if the user clearly wants a working outcome.

## What success looks like

A correct Feishu customization usually has to satisfy all of these:
- Feishu messages still send reliably
- normal answer streaming still works
- raw reasoning, if enabled, shows in the intended form
- final answer still closes correctly
- new sessions do not silently lose the behavior
- changes are documented so they can be rebuilt later

Do not optimize appearance first if delivery or runtime lane selection is broken.

## First pass: identify the real layer

Before editing anything, classify the issue into one of these layers:

1. Provider/runtime layer
- Model does not emit live reasoning events
- Reasoning is encrypted or only present in final transcript
- Provider silently falls back to a different model

2. Session/state layer
- New session lost `reasoningLevel=stream`
- Current session is using the wrong provider/model override
- Gateway service environment differs from shell environment

3. Feishu dispatcher layer
- `onReasoningStream` is wired incorrectly
- answer lane and reasoning lane are mixed
- snapshot reasoning is treated as delta and duplicates text
- final answer is suppressed or never overrides placeholder content

4. Card rendering layer
- wrong title/template/color
- panel folds at the wrong time
- placeholder is rendered in the wrong lane
- layout regresses from card 2.0 to plain markdown

5. Delivery layer
- streaming start fails
- reply API fails but direct send fallback works
- media/image sending path differs from text sending path

Do not assume a visual symptom is a card-layer problem. A "Thinking..." only state is often a runtime or session-state problem.

## Files to inspect first

Locate the installed OpenClaw package root first. In many environments it will be something like:

```bash
npm root -g
```

Then inspect these Feishu files first:
- `extensions/feishu/src/reply-dispatcher.ts`
- `extensions/feishu/src/streaming-card.ts`
- `extensions/feishu/src/send.ts`
- `extensions/feishu/src/outbound.ts`
- `extensions/feishu/src/channel.ts`
- `extensions/feishu/src/config-schema.ts`

Also inspect current runtime/session state:
- `~/.openclaw/openclaw.json`
- `~/.openclaw/agents/main/sessions/sessions.json`
- `~/.openclaw/logs/raw-stream.jsonl`

If symptoms do not match source edits, inspect the actual loaded runtime too:
- OpenClaw may be executing compiled `dist/` files, not `src/`

## Mandatory debugging workflow

Follow this order.

### 1. Confirm the active model path

Check all three, not just one:
- global default model in config
- current session provider/model override
- actual model/provider recorded in the current session transcript

Do not trust the agent saying "I switched models". Verify it in session files.

### 2. Confirm whether live reasoning exists at all

Look for evidence in:
- provider/runtime event logs
- `raw-stream.jsonl`
- current session transcript

Distinguish these cases:
- live reasoning event exists and is readable
- reasoning exists only in final transcript
- reasoning exists but is encrypted
- no reasoning exists at all

If the model does not produce readable live reasoning, Feishu cannot truly display raw reasoning no matter how good the card layer is.

#### Mandatory model capability check

Do not assume the current model supports visible raw reasoning.

Explicitly determine which of these four cases you are in:

1. **Readable live reasoning**
- runtime emits live reasoning text
- Feishu can display true raw reasoning if wired correctly

2. **Readable reasoning only in final transcript**
- no live reasoning events
- transcript contains thinking after completion
- Feishu cannot show true live raw reasoning without a shim/replay design

3. **Encrypted or opaque reasoning**
- reasoning exists only as encrypted/opaque payload
- Feishu cannot display raw reasoning directly

4. **No reasoning exposed**
- neither live events nor readable transcript thinking are available

For every model under investigation, verify all three:
- what the current session actually ran
- whether `raw-stream.jsonl` shows live thinking events
- whether the saved session transcript contains readable `thinking`

Only after this check may you decide whether the task is:
- a Feishu card implementation problem
- a session/runtime routing problem
- or a provider/model capability limit

#### How to explain the result to the user

After capability detection, always convert the result into one of these user-facing outcomes:

1. **Model supports raw reasoning**
- Say that raw reasoning can be implemented or repaired on the current model.
- Proceed to fix the Feishu card/runtime path.

2. **Model does not support readable raw reasoning, but supports normal streaming**
- Say that true raw reasoning is not available on the current model.
- Offer alternatives:
  - keep current model and improve card 2.0 appearance
  - switch to a model/provider path that supports raw reasoning

3. **Model/provider state is unclear**
- Say that the current route is not trustworthy yet.
- First fix routing/session state before making UI promises.

Do not just say "not supported" and stop. Turn it into the next actionable user choice.

### 3. Confirm session state

For Feishu direct sessions that should show raw reasoning, check:
- `reasoningLevel = stream`
- `thinkingLevel = low` or intended level

If new sessions keep dropping reasoning visibility, fix session initialization, not just the current session entry.

### 4. Confirm dispatcher wiring

For raw reasoning to display, the Feishu dispatcher must receive reasoning callbacks through the final reply options that runtime actually uses.

Do not attach `onReasoningStream` to the wrong layer.

If provider logs show thinking stream but Feishu only shows a static placeholder, inspect how `onReasoningStream` and `onReasoningEnd` are passed into the runtime.

### 5. Confirm card lane behavior

Keep reasoning and answer as separate lanes.

Typical correct structure:
- reasoning lane for thinking/raw reasoning
- answer lane for final answer

Do not keep placeholder text in the answer lane.

## Design rules for Feishu card customization

### Rule 1: Separate reasoning lane and answer lane

Raw reasoning and final answer should not share the same mutable text buffer.

Maintain separate state for:
- reasoning snapshot/current text
- answer snapshot/current text

This avoids:
- repeated reasoning
- reasoning leaking into answer
- final answer failing to replace the placeholder

### Rule 2: Treat reasoning snapshots carefully

Many runtimes emit cumulative reasoning snapshots, not pure deltas.

If each new reasoning frame includes all prior text, normalize it before streaming:
- detect whether the new text starts with the previous snapshot
- if so, only stream the appended suffix
- otherwise treat it as a replacement snapshot

Also normalize provider-added wrappers before diffing:
- leading `Reasoning:\n`
- outer `_..._`

### Rule 3: Use collapsible panels for reasoning, not for the main answer

For card 2.0 reasoning UX:
- put reasoning inside a `collapsible_panel`
- keep answer in a separate content element
- panel can start expanded
- collapse after reasoning ends and answer begins

Do not collapse immediately on `onReasoningEnd` if more reasoning or late answer frames may still arrive. Prefer delaying collapse until answer streaming actually begins.

### Rule 4: Keep the card title system unified

All message paths should share the same title/header strategy:
- normal card sends
- streaming card start
- streaming final close
- fallback direct sends
- image/media fallback card paths

If titles regress in only one path, inspect `outbound.ts` and fallback card builders.

### Rule 5: Fix the system, not a single task

If cron, new sessions, or fallback sends lose the behavior, repair the shared runtime/session/delivery logic.
Do not hardcode per-task fixes.

### Rule 6: Ask for text/style preferences when the problem is solved enough

Once delivery and runtime behavior are stable, invite the user to customize:
- title text
- panel title text
- color style
- whether reasoning should fold automatically
- whether group chats should differ from direct chats

Keep those questions simple and direct. For example:
- `主标题你想显示什么？`
- `思考面板标题你想写成“烟花在想”还是别的？`
- `颜色你想随机，还是固定一组偏好色？`

### Rule 7: Never restart the gateway silently

Do not restart `openclaw-gateway` on your own without telling the user.

If a restart is required:
- first explain why
- then either ask the user to run it
- or ask for confirmation before doing it

Use language like:
- `这个改动需要重启 gateway 才会生效。你来执行，还是我在你确认后替你执行？`

This rule exists because Feishu session behavior, active runs, and user expectations can all be disrupted by an unexpected restart.

## Current proven implementation pattern

When implementing raw reasoning plus card 2.0 behavior, use this architecture:

1. Keep normal Feishu streaming enabled
2. Add an explicit Feishu-level `reasoningStream` config gate
3. In the dispatcher:
- wire `onReasoningStream`
- wire `onReasoningEnd`
- keep a separate answer streaming path
4. In the streaming card:
- create a `collapsible_panel` for reasoning
- keep a separate answer element
- collapse the panel when answer streaming starts
5. Preserve reliable fallback sending if reply/update APIs fail
6. Ensure new Feishu direct sessions default to the intended reasoning state if the product requires it

## What to avoid

Avoid these anti-patterns:
- monkey-patching core dispatcher creation globally if a local reply option path is available
- forcing reasoning through unrelated block paths without evidence
- storing placeholders in answer lane
- editing only `src/` when runtime actually loads `dist/`
- trusting visual behavior without checking session/runtime logs
- trusting card appearance while ignoring delivery failures

## Validation checklist

Before claiming success, verify all of these:

1. A new Feishu direct session uses the intended model
2. A new Feishu direct session has the intended reasoning state
3. Raw reasoning displays without repeated snapshot spam
4. Final answer still streams
5. Reasoning panel collapses at the right time
6. Titles/templates/colors are consistent across:
- streaming
- final answer
- fallback text send
- fallback media/image send
7. Restarting the gateway does not drop the behavior
8. Creating a new session does not drop the behavior
9. The tested model was confirmed to expose readable live reasoning, or the limitation was explicitly documented

## Documentation requirement

Every meaningful Feishu card customization must update the project’s Feishu card guide or create one if absent.

Document at minimum:
- the user-facing goal
- the actual root cause
- exact files changed
- required session/runtime conditions
- known model/provider limits
- how to verify after restart
- how to recover if the behavior drops again

## Suggested output when using this skill

When you finish, report in this order:

1. Root cause
2. What layer was fixed
3. What files changed
4. What was verified
5. What can still regress and how to check it

If the issue is only partially solvable because of model/provider limits, also include:
6. What still can be customized anyway
7. What user-facing choices are available next

## Examples of prompts that should trigger this skill

Example 1:
`帮我把 OpenClaw 的飞书回复卡片改得更像一个完整 UI，不要只有一块 markdown。`

Example 2:
`之前飞书里能流 raw reasoning，今天又只剩 Thinking... 了，你帮我恢复。`

Example 3:
`把飞书思考过程做成折叠面板，思考完自动折叠，再开始流正式回复。`

Example 4:
`为什么飞书里只有部分路径的标题还是旧的“烟花想法”，帮我统一掉。`

Example 5:
`帮我看看这个模型到底支不支持在飞书里流 raw reasoning，不要先默认是卡片代码的问题。`

## Example prompts and expected behaviors

Use these as practical calibration examples. They are not heavy formal evals; they exist to keep the skill usable and consistent.

### Example A: Raw reasoning disappeared

Prompt:
`昨天还能看到飞书里流 raw reasoning，今天又只剩 Thinking... 了，帮我查一下。`

Expected behavior:
- inspect model/session/runtime before changing card visuals
- verify whether the current session lost `reasoningLevel=stream`
- explain the root cause in plain language
- if the model cannot provide readable live reasoning, say so clearly and offer alternatives

### Example B: User wants style customization

Prompt:
`我想把飞书卡片标题改成别的文案，再加一点颜色。`

Expected behavior:
- avoid over-diagnosing if delivery/runtime is already healthy
- ask direct preference questions:
  - title text
  - reasoning panel title
  - random vs fixed color style
- implement styling in the correct Feishu card builder path
- keep fallback paths visually consistent

### Example C: Model does not support raw reasoning

Prompt:
`为什么这个模型只有回答流，没有 raw reasoning？还能做点什么？`

Expected behavior:
- explicitly classify the model as:
  - supports readable live reasoning
  - transcript-only thinking
  - encrypted/opaque reasoning
  - no reasoning exposed
- do not pretend Feishu alone can fix a provider limitation
- offer alternatives:
  - keep current model and improve card 2.0 appearance
  - switch to a model/path that supports raw reasoning

### Example D: Needs restart to take effect

Prompt:
`你直接帮我把飞书卡片改掉。`

Expected behavior:
- make the code/config changes
- if restart is required, do not restart silently
- tell the user what changed and say:
  - why restart is needed
  - whether the user should run it
  - or ask for confirmation before doing it

### Example E: New session keeps losing the behavior

Prompt:
`每次 /new 之后 raw reasoning 就没了。`

Expected behavior:
- do not patch only the current session
- inspect session initialization/default inheritance
- fix the shared session/runtime path so future sessions retain the intended state
