---
name: memphis
description: Memphis AI brain integration - local-first memory with journal, recall, ask, decisions, and summaries
---

# Memphis Brain Skill

Integracja pamięci Memphis — lokalne dzienniki, przypomnienia, decyzje i streszczenia w jednym CLI.
Ten dokument opisuje, jak korzystać z komend, kiedy przełączać modele i jakie są role agentów.

## Szybki przegląd komend

| Komenda | Opis | Przykład | Uwagi |
|---------|------|----------|-------|
| `memphis journal` | Zapisz zapis dziennika / decyzję | `memphis journal "Decyzja: zrobimy refaktoryzację" --tags decision` | Automatycznie wykrywa decyzje; dodaj `--tags` dla kontekstu |
| `memphis ask` | Zapytaj o kontekst z pamięcią | `memphis ask "Co planowałem w sprawie TUI?"` | Używa pełnego kontekstu; dodaj `--prefer-summaries` gdy chcesz zwięzłą wersję |
| `memphis recall` | Wyszukaj wpisy | `memphis recall "deploy" --tag friction` | Możesz filtrować tagami, łańcuchami (
`--chain decision`
) |
| `memphis status` | Sprawdź zdrowie systemu | `memphis status --json` | Przydatne jako poranne odpalenie; `--json` dla integracji |
| `memphis summarize` | Streszczenie pamięci | `memphis summarize --force` | `--dry-run` symuluje podsumowanie bez zapisu |
| `memphis tui` | Interaktywne TUI | `memphis tui` → naciśnij `S` dla podsumowania | Używaj podczas burzy mózgów / retrospektywy |

## Typowy workflow

1. **Rano** – `memphis status` dla szybkiego wglądu w zdrowie systemu.
2. **W ciągu dnia** – `memphis journal "..."` dla notatek, wniosków i decyzji.
3. **Podczas myślenia** – zamiast Google: `memphis ask "..."` (przypomnienia + kontekst).
4. **Szukając szczegółów** – `memphis recall "keyword"` lub dodaj `--chain decision` dla decyzji.
5. **Podsumowania** – `memphis summarize --force` albo `memphis tui` → `S`.
6. **Zarządzanie problemami** – `memphis journal "FRICTION: opis | oczekiwany rezultat" --tags friction`. 

## Model selection — kiedy który model

Styl (Style) i subagenci wielokrotnie muszą wybrać, który model najlepiej pasuje do zadania. Oto zasady:

| Cel | Model | Kiedy używać | Dlaczego |
|-----|-------|--------------|----------|
| **Kreatywna rozmowa / planowanie / tłumaczenia** | `minimax-portal/MiniMax-M2.5` (MiniMax) | Gdy rozmawiamy z użytkownikiem lub tworzymy narrację | Domyślny model; najlepiej radzi sobie z kontekstem i tonem |
| **Szybkie poprawki / małe fragmenty kodu** | `openai/gpt-5.1-codex-mini` (Codex Mini) | Jeden plik, proste zmiany, krótkie funkcje, formatowanie | Szybki, tani, wystarczający do prostych zadań |
| **Złożona refaktoryzacja / debug / multi-file** | `openai/gpt-5.1-codex` (Codex 5.1) | Gdy potrzebna jest głęboka analiza kodu, wieloetapowe podejście | Więcej kontekstu i lepsze rozumienie zależności |

**Notatka:** Style zawsze pilnuje, by model dopasował się do celu zadania. Jeśli zadanie zaczyna się w MiniMax, ale szybko staje się kodowe, następuje przekazanie (auto-switch).

## Auto-switching — kiedy i dlaczego zmieniam model

Przykłady, kiedy Style lub subagent przełączają model w trakcie rozmowy:

1. **Zadanie zaczyna się od opisu**: Użytkownik opisuje problem w MiniMax, ale prosi o zmianę pliku konfiguracyjnego → subagent `codex-mini` wykonuje edycję.
2. **Nieprzewidziana złożoność**: Początkowy request to "dodaj log" (Codex Mini). Gdy okazuje się, że potrzebujemy naprawić całą klasę logowania, przekierowujemy do `codex`.
3. **Przekazywanie od Style do subagenta**: Style analizuje kontekst (Model: MiniMax), wykrywa konieczność kodowania i uruchamia subagenta z `sessions_spawn()` na `openai/gpt-5.1-codex-mini`, informując użytkownika "Używam Codex Mini dla tego zadania".
4. **Zmiana po analizie**: Subagent pracuje na konkretnym fragmencie, ale w trakcie odkrywa zależności w innych plikach → eskaluje do `Codex 5.1` albo prosi Style o pomoc.

Auto-switch nie oznacza chaosu — zawsze podajemy użytkownikowi aktualny model i krótko uzasadniamy wybór.

## Aktualne modele i ich zastosowania

| Model | Skrót | Główne zastosowania | Uwagi |
|-------|------|---------------------|-------|
| `minimax-portal/MiniMax-M2.5` | MiniMax | Dialog, planowanie, pytania otwarte, pomaganie Style | Domyślny model konwersacyjny, duża pamięć kontekstu |
| `openai/gpt-5.1-codex-mini` | Codex Mini | Proste poprawki kodu, szybkie commity, formatowanie | Najtańszy model kodowy; idealny do jednej funkcji |
| `openai/gpt-5.1-codex` | Codex 5.1 | Refaktoryzacje, analiza architektury, debug | Gdy potrzebne głębokie zrozumienie wielu plików |

## Role agentów

- **Style (agent główny)** – odpowiada za narrację, tłumaczenia, komunikację, planowanie modeli oraz przekazy. Zna historię (pamięć), pilnuje tonu, decyduje o auto-switchingu i potrafi spawnować subagentów CLI.
- **Subagent** – wyspecjalizowany w jednym zadaniu (np. refaktoryzacja). Styl (Style) przekazuje kontekst i model, subagent wykonuje kodowe zmiany w odpowiednim środowisku.

## Consistency: Polish / English mix

- Komendy pozostają w języku angielskim (CLI używa języka angielskiego).
- Opisy i narracje są głównie po polsku, by utrzymać spójność z dokumentacją użytkownika.
- W przypadku cytatów (np. "Używam Codex Mini dla tego zadania") stosujemy polskie frazy celowo.

---
Jeśli chcesz rozbudować dokumentację (np. więcej przykładowych tagów), dopisz kolejną sekcję.
