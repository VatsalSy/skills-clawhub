---
name: effortlist-ai
description: Manage EffortList AI folders, tasks, and todos. Use when the user wants to organize their life, track projects, or manage schedules via the EffortList AI platform. Supports full CRUD operations, cascading deletes, and atomic undo/redo history for data integrity.
metadata:
  {
    "homepage": "https://www.effortlist.io",
    "openclaw": { "requires": { "env": ["EFFORTLIST_API_KEY"] } },
  }
---

# 📋 EffortList AI Agent Skill

**EffortList AI** is a sophisticated life-management platform that merges advanced Generative AI with a robust, deterministic scheduling engine. It goes beyond simple to-do lists by utilizing an "Omni" engine for managing entire to-do list life cycles and managing complex schedules all in one place.

---

## 🚀 Setup & Authentication

Access to the Developer API requires an active account and a developer subscription.

1.  **Create Account:** Join at [effortlist ai website](https://www.effortlist.io).
2.  **Subscribe:** A minimun subscription of **$5/month** is required to unlock the Developer APIs and full CRUD operations for agents.
3.  **Generate Key:** Create a **Persistent API Key** in the **Developer Settings** within the app.
4.  **Configure Agent:** Provide your key to the agent via a secure environment variable: `EFFORTLIST_API_KEY`.

> [!IMPORTANT]
> **Variable Name:** `EFFORTLIST_API_KEY`
> **Storage:** Use OpenClaw's secure credential store or your system's environment variables. **Never** store your key in plaintext files.

---

## 🧠 Core Intelligence & Logic

EffortList AI operates on a **Hybrid AI** model:

- **Omni Engine:** Powered by Gemini for intent classification, prompt decomposition, and parallel task processing.
- **Deterministic Precision:** Uses code libraries (RRule) for 100% accurate recurrence and date math.
- **Intelligent Scheduling:** Proactively protects break times and utilizes "Gap-First" placement for new events.
- **Reminders vs. Todos:** Reminders (`isReminder: true`) are notifications; Todos are actionable items that occupy time slots.

---

## 📐 Data Hierarchy

- 📁 **Folders:** Optional top-level containers for grouping projects.
- 📋 **Tasks:** Actionable projects. Can be top-level (null `folderId`) or nested in a folder.
- ✅ **Todos:** Granular actionable steps. **Every Todo must have a parent Task.**

---

## 🛠️ Best Practices for Agents

- **⚡ Optimized Lookups:** Always use `folderId` (for tasks) or `taskId` (for todos) for blazingly fast database-level filtering.
- **🎯 Surgical Extraction:** Use the `?id=<ID>` parameter to fetch single specific records efficiently.
- **↩️ Atomic Safety:** Every `POST` and `DELETE` is tracked. Use `POST /api/v1/undo` to revert actions (including cascading deletes) atomically.
- **🌐 Production Target:** The canonical base URL for all requests is `https://effortlist.io/api/v1`.

---

## 🖥️ Example Usage

```bash
# Create a new top-level task
curl -X POST "https://effortlist.io/api/v1/tasks" \
  -H "Authorization: Bearer $EFFORTLIST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Quantum Research", "folderId": null}'
```

---

## 🔒 Security & Privacy

EffortList AI is built with a **Zero Trust** architecture:

- **Data Isolation:** Strict row-level security ensures users only see their own data.
- **Encryption:** All data is encrypted at rest (AES-256) and in transit (TLS 1.3).
- **AI Privacy:** Your data is **never** used to train AI models. Processing is done via enterprise-tier APIs.

For a full security audit, refer to [Security](https://www.effortlist.io/security).

---

For technical endpoint details and response schemas, refer to [Docs](https://www.effortlist.io/docs).
