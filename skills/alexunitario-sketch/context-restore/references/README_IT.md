# Context Restore Skill - Guida Italiana
# Context Restore Skill - Italian Guide

---

## Trigger / Trigger / 触发

- `ripristina contesto`
- `continua`
- `riprendi`
- `ripristina sessione`
- `continua il lavoro precedente`

---

## Livelli di Recupero / 恢复级别 / Recovery Levels

### minimal / 最小
- Solo il nome del task attuale
- Output: 1-2 righe
- Per recovery rapidi

### normal (predefinito) / 正常（默认）
- Task attuale + operazioni recenti
- Output: 3-5 righe strutturate
- Bilanciato

### detailed / 详细
- Tutte le informazioni contestuali
- Include dettagli progetto, cronologia, todo
- Output completo

---

## Utilizzo / 使用 / Usage

### Esempio 1: Recovery Base
```
Input: ripristina contesto
Output: ✅ Contesto ripristinato
        Task: Completare API documentation
        Progetto: Backend-API-v2
```

### Esempio 2: Recovery Dettagliato
```
Input: ripristina contesto --dettagliato
Output: ✅ Contesto ripristinato (dettagliato)

📋 Task Attuale
- Nome: Completare API documentation
- Priorità: Alta
- Scadenza: 2026-02-10

🔧 Progetti
- Nome: Backend-API-v2
- Stato: In sviluppo
- Completamento: 75%

📝 Operazioni Recenti
1. Completato modulo auth (2 ore fa)
2. Fixato bug login (ieri)
```

### Esempio 3: Recovery Minimo
```
Input: continua
Output: ✅ → Completare API documentation
```

---

## Integrazione / 配合 / Integration

### memory_get
Dopo il ripristino, usa `memory_get` per cronologia completa.

### memory_search
Quando servono informazioni specifiche non nel contesto.

### sessions_spawn
Per creare nuove sessioni basate sul contesto ripristinato.

---

## Errori Comuni / 常见错误 / Common Errors

- ❌ `Nessuna sessione contesto salvata trovata`
- ⚠️ `File contesto corrotto`
- 🚫 `Impossibile accedere al file contesto`

---

## Best Practice

✅ Usa il livello `normal` per la maggior parte dei casi
✅ Combina con `memory_get` per contesto completo
❌ Non usare `detailed` per controlli rapidi
