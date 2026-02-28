---
name: ranking-of-claws
description: "Reports token usage to the Ranking of Claws leaderboard"
metadata:
  openclaw:
    emoji: "👑"
    events: ["message:sent"]
---

# Ranking of Claws Hook

Listens to message:sent events, accumulates tokens, and reports hourly to the leaderboard API.
