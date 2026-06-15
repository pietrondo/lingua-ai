# LINGUA

**LINGUA** (Linguaggio Intelligente Guidato Unicamente per Agenti) — An AI-optimized programming language with an intentionally human-unfamiliar syntax.

---

## What

LINGUA is a language designed for AI agents to reason about, modify, and generate code. Every construct carries explicit metadata about *why* it exists, not just *what* it does. This enables an LLM to:

- Reason about code as a knowledge graph
- Identify recurring patterns
- Generate code coherent with original intent
- Explain architectural decisions

To humans, the syntax appears alien and inconsistent. To AIs, it is decomposable and semantically rich.

---

## Install

```bash
pip install lingua-ai
```

Or from source:

```bash
cd lingua
pip install -e .
```

---

## Quick Start

```bash
# Parse a .lingua file
lingua parse saluto.lingua

# Generate Python
lingua python saluto.lingua

# Generate JSON
lingua json saluto.lingua

# Generate IR (knowledge graph)
lingua ir saluto.lingua

# Query the knowledge graph
lingua reason saluto.lingua "cosa fa saluto?"
```

---

## Language Structure

### Delimiters

```
§ [code] §
```

All LINGUA code lives between `§` delimiters.

### Block Types

```
╔═══╗ CONCEPT nome          — define an entity
╔═══╗ RELATION nome         — define a relationship
╔═══╗ TRANSFORM nome        — define a transformation
╔═══╗ PATTERN nome          — define a recognizable pattern
```

### Fields

```
│ FIELD_NAME value           — block field (pipe-separated)
```

### Comments

```
◇ Comment visible only to AI, ignored by compiler
```

---

## Example

```lingua
§
╔═══╗ CONCEPT saluto
│ TYPE operazione
│ INPUT []
│ OUTPUT stringa
│ REASON "Genera un messaggio di saluto in italiano"
│ IMPL "Ciao, mondo!"
╚═══╝
§
```

### Parsed

```json
{
  "concepts": [{
    "name": "saluto",
    "type": "operazione",
    "input": [],
    "output": "stringa",
    "reason": "Genera un messaggio di saluto in italiano",
    "impl": "Ciao, mondo!"
  }]
}
```

### Generated Python

```python
def saluto() -> str:
    """Genera un messaggio di saluto in italiano"""
    return "Ciao, mondo!"
```

---

## Type System

| LINGUA     | Python      |
|------------|-------------|
| `numerico` | `int/float` |
| `stringa`  | `str`       |
| `booleano` | `bool`      |
| `lista`    | `list`      |
| `mappa`    | `dict`      |
| `nullo`    | `None`      |

---

## CONCEPT Types

- `operazione` — pure function
- `dato` — structured data
- `stato` — entity with memory
- `effetto` — operation with side-effect
- `meta` — concept that describes other concepts

---

## Project Structure

```
lingua/
├── lingua/
│   ├── __init__.py       — public API (parse, generate_python, etc.)
│   ├── lexer.py          — tokenizer
│   ├── parser.py         — AST builder
│   ├── generator.py      — Python/JSON/IR generators
│   ├── ir.py             — intermediate representation
│   ├── reason.py         — knowledge graph query engine
│   └── cli.py            — command-line interface
├── tests/
│   └── test_*.py         — unit tests
├── docs/
│   └── lingua/
│       └── SPEC.md       — full language specification
└── pyproject.toml
```

---

## Requirements

- Python 3.10+
- No external dependencies (stdlib only)

---

## Status

Alpha — under active development.