---
name: context-restore
description: |
  EN: Triggered when user says "restore context", "continue", or similar in English.
  ZH: 当用户说中文"恢复上下文"、"恢复"、"接着"、"继续之前的工作"时触发。
  IT: Si attiva quando l'utente dice "ripristina contesto", "continua" in italiano.

  Reads compressed context files, extracts key info (recent operations, projects, tasks),
  读取压缩上下文文件，提取关键信息（最近操作、核心项目、当前任务），
  Legge i file di contesto compressi, estrae info chiave (operazioni recenti, progetti, task).

  Works with memory_get, memory_search for complete memory management.
  与 memory_get、memory_search 配合使用，形成完整的记忆管理系统。
  Funziona con memory_get, memory_search per una gestione completa della memoria.
---

## [EN] Triggers / [ZH] 触发条件 / [IT] Trigger

### [EN] English Keywords
### [ZH] 中文关键词
### [IT] Parole chiave italiane

- **EN**: restore context, continue, continue previous work, resume, restore session
- **ZH**: 恢复上下文, 恢复, 接着, 继续之前的工作, 继续之前, 接着之前的工作
- **IT**: ripristina contesto, continua, riprendi, ripristina sessione

---

## [EN] Execution Flow / [ZH] 执行流程 / [IT] Flusso di Esecuzione

### [EN] Step 1: Detect Context Files
### [ZH] 步骤 1：检测上下文文件
### [IT] Passo 1: Rileva file di contesto

**[EN]** Scans predefined context storage locations for compressed context files (typically `.context.gz` or similar format).
**[ZH]** 扫描预定义的上下文存储位置，查找压缩的上下文文件（通常为 `.context.gz` 或类似格式）。
**[IT]** Scansiona le posizioni di archiviazione contesto predefinite, cercando file di contesto compressi (tipicamente `.context.gz` o formato simile).

### [EN] Step 2: Decompress and Parse
### [ZH] 步骤 2：解压与解析
### [IT] Passo 2: Decomprimi e analizza

**[EN]** Decompress context files and parse JSON/YAML structure, extracting key fields.
**[ZH]** 解压上下文文件并解析其中的 JSON/YAML 结构，提取关键字段。
**[IT]** Decomprimi i file di contesto e analizza la struttura JSON/YAML, estraendo i campi chiave.

### [EN] Step 3: Information Aggregation
### [ZH] 步骤 3：信息聚合
### [IT] Passo 3: Aggregazione informazioni

**[EN]** Integrate extracted information into a structured context summary.
**[ZH]** 将提取的信息整合为结构化的上下文摘要，便于快速理解当前状态。
**[IT]** Integra le informazioni estratte in un riepilogo contestuale strutturato.

### [EN] Step 4: Send Confirmation
### [ZH] 步骤 4：发送确认消息
### [IT] Passo 4: Invia conferma

**[EN]** Send confirmation message to user with brief status description.
**[ZH]** 向用户发送确认消息，告知上下文已恢复，并简要说明当前状态。
**[IT]** Invia messaggio di conferma all'utente, informando che il contesto è stato ripristinato.

---

## [EN] Recovery Levels / [ZH] 恢复级别 / [IT] Livelli di Recupero

### [EN] minimal / [ZH] 最小 / [IT] minimo
**[EN]** Only restores current task name, 1-2 lines confirmation.
**[ZH]** 仅恢复当前任务名称，输出 1-2 行简要确认。
**[IT]** Ripristina solo il nome del task attuale, conferma di 1-2 righe.

### [EN] normal (default) / [ZH] 正常（默认） / [IT] normale (predefinito)
**[EN]** Restores current task + recent operations, 3-5 lines structured summary.
**[ZH]** 恢复当前任务 + 最近操作，输出 3-5 行结构化摘要。
**[IT]** Ripristina task attuale + operazioni recenti, riepilogo strutturato di 3-5 righe.

### [EN] detailed / [ZH] 详细 / [IT] dettagliato
**[EN]** Restores all context info including project details, task history, todos.
**[ZH]** 恢复所有上下文信息，包括项目详情、任务历史、待办事项。
**[IT]** Ripristina tutte le informazioni contestuali inclusi dettagli progetto, cronologia task, cose da fare.

---

## [EN] Integration with Other Skills / [ZH] 与其他技能的配合 / [IT] Integrazione con altre Skill

### [EN] memory_get
**[EN]** Call after context restore for detailed history.
**[ZH]** 在恢复上下文后，可调用获取更详细的历史记录。
**[IT]** Chiama dopo il ripristino contesto per cronologia dettagliata.

### [EN] memory_search
**[EN]** Use when context file is insufficient for user questions.
**[ZH]** 上下文文件不足以回答用户问题时使用。
**[IT]** Usa quando il file contesto non basta per le domande dell'utente.

### [EN] sessions_spawn
**[EN]** Use when needing to create new sessions based on restored context.
**[ZH]** 当需要基于恢复的上下文创建新会话时使用。
**[IT]** Usa quando servono nuove sessioni basate sul contesto ripristinato.

---

## [EN] Output Format / [ZH] 输出格式 / [IT] Formato di Output

### [EN] Standard Confirmation Message
### [ZH] 标准确认消息格式
### [IT] Messaggio di conferma standard

```
✅ [EN] Context restored / [ZH] 上下文已恢复 / [IT] Contesto ripristinato

[EN] Task summary / [ZH] 任务摘要 / [IT] Riepilogo task
[EN] Project info / [ZH] 项目信息 / [IT] Informazioni progetto
[EN] Recent operations / [ZH] 最近操作 / [IT] Operazioni recenti

> [EN] Use memory_get for more info / [ZH] 可选：使用 memory_get 获取更多信息 / [IT] Usa memory_get per più info
```

### [EN] Error Handling / [ZH] 错误处理 / [IT] Gestione Errori

- **[EN]** No context file: `❌ No saved context session found`
- **[ZH]** 无上下文文件：`❌ 未找到保存的上下文会话`
- **[IT]** Nessun file contesto: `❌ Nessuna sessione contesto salvata trovata`

- **[EN]** File corrupted: `⚠️ Context file corrupted`
- **[ZH]** 文件损坏：`⚠️ 上下文文件已损坏`
- **[IT]** File corrotto: `⚠️ File contesto corrotto`

- **[EN]** Permission error: `🚫 Cannot access context file`
- **[ZH]** 权限错误：`🚫 无法访问上下文文件`
- **[IT]** Errore permessi: `🚫 Impossibile accedere al file contesto`
