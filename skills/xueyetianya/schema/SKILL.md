---
name: schema
version: "1.0.0"
description: "Design and manage database schemas using CLI tools. Use when you need to create tables, columns, indexes, relations, validate, migrate, diff,"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags:
  - database
  - schema
  - design
  - migration
  - sql
---

# Schema — Database Schema Design Tool

A thorough CLI tool for designing, managing, and evolving database schemas. Supports table creation, column management, indexing, relationship mapping, validation, migration generation, schema diffing, and import/export — all stored locally in JSONL format.

## Prerequisites

- Python 3.8+
- Bash shell
- `jq` (optional, for pretty JSON output)

## Data Storage

All schema data is persisted in `~/.schema/data.jsonl`. Each line is a JSON object representing a schema entity (table, column, index, or relation). This enables easy versioning, diffing, and portability.

## Commands

Run all commands via the script at `scripts/script.sh`.

### `create`
Create a new schema/database namespace.
```bash
bash scripts/script.sh create <schema_name> [--charset utf8mb4] [--engine InnoDB]
```

### `table`
Create or manage a table within a schema.
```bash
bash scripts/script.sh table <schema_name> <table_name> [--if-not-exists]
```

### `column`
Add, modify, or remove a column from a table.
```bash
bash scripts/script.sh column <schema_name> <table_name> <column_name> <type> [--nullable] [--default value] [--primary] [--unique] [--remove]
```

### `index`
Create or drop an index on a table.
```bash
bash scripts/script.sh index <schema_name> <table_name> <index_name> <columns> [--unique] [--drop]
```

### `relation`
Define a foreign-key relationship between tables.
```bash
bash scripts/script.sh relation <schema_name> <from_table.column> <to_table.column> [--type one-to-many] [--on-delete CASCADE]
```

### `validate`
Validate a schema for integrity issues (missing references, orphan columns, duplicate indexes).
```bash
bash scripts/script.sh validate <schema_name>
```

### `migrate`
Generate SQL migration statements from current schema state.
```bash
bash scripts/script.sh migrate <schema_name> [--format sql|json] [--dialect mysql|postgres|sqlite]
```

### `diff`
Compare two schemas and show differences.
```bash
bash scripts/script.sh diff <schema_a> <schema_b>
```

### `export`
Export a schema to JSON or SQL format.
```bash
bash scripts/script.sh export <schema_name> [--format json|sql|yaml]
```

### `import`
Import a schema definition from a JSON file.
```bash
bash scripts/script.sh import <file_path> [--schema_name override_name]
```

### `help`
Show usage information and available commands.
```bash
bash scripts/script.sh help
```

### `version`
Show the current version of the schema tool.
```bash
bash scripts/script.sh version
```

## Workflow Example

```bash
# Create a schema
bash scripts/script.sh create myapp --charset utf8mb4

# Add tables
bash scripts/script.sh table myapp users
bash scripts/script.sh table myapp posts

# Add columns
bash scripts/script.sh column myapp users id INTEGER --primary
bash scripts/script.sh column myapp users email VARCHAR --unique
bash scripts/script.sh column myapp posts id INTEGER --primary
bash scripts/script.sh column myapp posts user_id INTEGER

# Add relation
bash scripts/script.sh relation myapp posts.user_id users.id --type one-to-many

# Validate
bash scripts/script.sh validate myapp

# Generate migration
bash scripts/script.sh migrate myapp --dialect postgres
```

## Notes

- All data is local — no database connection required for design phase.
- Schema definitions are portable via export/import.
- Validation catches common design issues before migration.
- Supports MySQL, PostgreSQL, and SQLite dialects for migration output.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
