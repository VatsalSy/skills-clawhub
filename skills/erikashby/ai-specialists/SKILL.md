---
name: ai-specialists
description: Interact with AI Specialists via the AI Specialists Hub MCP endpoint. Use when the user asks about any of their AI specialists (e.g. Ruby, Peter, Benjamin, Marty), wants to read/write specialist documents, manage meal plans, check specialist workspaces, hire/dismiss specialists, or work with any MCP-connected specialist. Also use when the user mentions "specialist", "AI specialist", "MCP", or refers to a specialist by name.
---

# AI Specialists Hub - MCP Integration

## Connection

Call the MCP endpoint via HTTP POST. The endpoint URL is stored in TOOLS.md or provided by the user.

```bash
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"TOOL_NAME","arguments":{...}}}'
```

**Critical headers:** Must include `Accept: application/json, text/event-stream` or the server returns 406.

**Response format:** SSE — parse with: `response.split('data: ')[1]` → JSON → `result.content[0].text`

## Available Tools

### Discovery & Management
| Tool | Required Params | Description |
|------|----------------|-------------|
| `list_specialists` | — | List all hired specialists |
| `list_specialist_types` | — | List available specialist types |
| `hire_specialist` | `type`, `name` | Hire a new specialist |
| `dismiss_specialist` | `specialist` | Remove a specialist |
| `import_specialist` | `url` | Import from GitHub URL |
| `get_specialist_overview` | `specialist` | Get specialist summary |

### Workspace Navigation
| Tool | Required Params | Description |
|------|----------------|-------------|
| `explore_specialist_tree` | `specialist` | Full folder/file tree |
| `list_specialist_folder` | `specialist`, `folder_path` | List folder contents |

### Document Operations
| Tool | Required Params | Description |
|------|----------------|-------------|
| `read_specialist_document` | `specialist`, `document_path` | Read one document |
| `read_specialist_documents` | `specialist`, `document_paths` (array) | Bulk read multiple docs |
| `update_specialist_document` | `specialist`, `document_path`, `content` | Create or update a doc |
| `delete_specialist_document` | `specialist`, `document_path` | Delete a document |

### Folder Operations
| Tool | Required Params | Description |
|------|----------------|-------------|
| `create_specialist_folder` | `specialist`, `folder_path` | Create folder (recursive) |
| `delete_specialist_folder` | `specialist`, `folder_path` | Delete folder and contents |

**Parameter note:** The specialist identifier is always the `id` field from `list_specialists`, not the display name. Use lowercase (e.g. `ruby`, `peter`, `benjamin`).

## Working with a Specialist

Every specialist has an `ai-instructions/` folder containing their identity and behavioral instructions. **Always read these first** when working with a specialist you haven't loaded yet:

```
ai-instructions/
├── core-instructions.md    # Who they are, what they do, how they behave
└── getting_started.md      # Initialization sequence, workspace structure
```

### Pattern: First interaction with a specialist

1. `list_specialists` → find the specialist id
2. `read_specialist_documents` → read `ai-instructions/core-instructions.md` and `ai-instructions/getting_started.md`
3. Understand their domain, workspace structure, and communication style
4. `explore_specialist_tree` → see their full workspace
5. Now you can work with their data informed by their context

### Pattern: Quick data retrieval

1. `explore_specialist_tree` → find the files you need
2. `read_specialist_documents` → bulk read (more efficient than individual reads)
3. Summarize for the user

### Pattern: Updating specialist data

1. Read the existing document first
2. Modify content as needed
3. `update_specialist_document` → write back (creates if new, overwrites if existing)
4. For new folders: `create_specialist_folder` first, then write documents into it

## Configuration

Store the MCP endpoint URL in TOOLS.md:

```markdown
### AI Specialists Hub
- MCP endpoint: https://aispecialistshub.com/api/v1/mcp/<user>/<key>
```

See `references/specialists-guide.md` for details on specialist workspace conventions.
