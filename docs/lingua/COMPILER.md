# LINGUA Compiler — Architettura Tecnica

**Versione:** 1.0.0  
**Data:** 2026-06-15

---

## Panoramica

Il compilatore LINGUA trasforma codice LINGUA in:
- **Python 3** — esecuzione diretta
- **JSON** — debugging e analisi AI
- **IR** — Intermediate Representation per ottimizzazioni

---

## Architettura a Fasi

```
Codice LINGUA (testo)
        │
        ▼
   ┌─────────┐
   │  Lexer  │  Tokenizzazione
   └────┬────┘
        │ Token stream
        ▼
   ┌─────────┐
   │  Parser  │  Parsing -> AST
   └────┬────┘
        │ AST
        ▼
   ┌─────────────────┐
   │ Reasoning Engine │  Validazione semantica
   └────────┬────────┘
            │ AST validato
            ▼
   ┌──────────────────┐
   │  Code Generator  │  Generazione output
   └──────────────────┘
            │
    ┌───────┼───────┐
    ▼       ▼       ▼
  Python    JSON     IR
```

---

## Fase 1: Lexer

### Responsabilità
- Leggere il codice carattere per carattere
- Produrre una lista di token

### Token Types

```python
TOKENS = {
    'DELIMITER_OPEN':   '§',
    'DELIMITER_CLOSE':  '§',
    'BLOCK_OPEN':       '╔═══╗',
    'BLOCK_CLOSE':      '╚═══╝',
    'SEPARATOR':        '│',
    'COMMENT':          '◇',
    'CONCEPT':          'CONCEPT',
    'RELATION':         'RELATION',
    'TRANSFORM':        'TRANSFORM',
    'PATTERN':          'PATTERN',
    'TYPE':             'TYPE:',
    'INPUT':            'INPUT:',
    'OUTPUT':           'OUTPUT:',
    'REASON':           'REASON:',
    'IMPL':             'IMPL:',
    'FROM':             'FROM:',
    'TO':               'TO:',
    'CAUSE':            'CAUSE:',
    'EFFECT':           'EFFECT:',
    'PRESERVE':         'PRESERVE:',
    'CONSTRAINT':       'CONSTRAINT:',
    'MAP':              'MAP:',
    'EVIDENCE':         'EVIDENCE:',
    'CONTEXT':          'CONTEXT:',
    'RESOLVE':          'RESOLVE:',
    'IDENTIFIER':       r'[a-zA-Z_][a-zA-Z0-9_]*',
    'STRING':           r'"[^"]*"',
    'NUMBER':           r'\d+(\.\d+)?',
    'LBRACKET':         '[',
    'RBRACKET':         ']',
    'LBRACE':           '{',
    'RBRACE':           '}',
    'NEWLINE':          '\n',
    'EOF':              'EOF',
}
```

### Output del Lexer

```python
class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
```

---

## Fase 2: Parser

### Responsabilità
- Costruire l'AST dai token
- Validare la struttura sintattica

### AST Nodes

```python
class ConceptNode:
    def __init__(self, name, type, input_types, output_type, reason, impl):
        self.name = name
        self.type = type
        self.input_types = input_types
        self.output_type = output_type
        self.reason = reason
        self.impl = impl

class RelationNode:
    def __init__(self, name, from_concept, to_concept, rel_type, reason):
        self.name = name
        self.from_concept = from_concept
        self.to_concept = to_concept
        self.rel_type = rel_type
        self.reason = reason

class TransformNode:
    def __init__(self, name, cause, effect, preserve, constraint, map_rule):
        self.name = name
        self.cause = cause
        self.effect = effect
        self.preserve = preserve
        self.constraint = constraint
        self.map_rule = map_rule

class PatternNode:
    def __init__(self, name, evidence, context, resolve):
        self.name = name
        self.evidence = evidence
        self.context = context
        self.resolve = resolve
```

### Parsing Rules

```
program        ::= DELIMITER_OPEN statements DELIMITER_CLOSE
statements     ::= statement (SEPARATOR statement)*
statement      ::= concept | relation | transform | pattern
concept        ::= BLOCK_OPEN CONCEPT IDENTIFIER fields BLOCK_CLOSE
relation       ::= BLOCK_OPEN RELATION IDENTIFIER fields BLOCK_CLOSE
transform      ::= BLOCK_OPEN TRANSFORM IDENTIFIER fields BLOCK_CLOSE
pattern        ::= BLOCK_OPEN PATTERN IDENTIFIER fields BLOCK_CLOSE
fields        ::= (SEPARATOR field)*
field         ::= FIELD_NAME field_value
field_value   ::= STRING | list | IDENTIFIER
list          ::= LBRACKET (field_value ("," field_value)*)? RBRACKET
```

---

## Fase 3: Reasoning Engine

### Responsabilità
- Validare la coerenza semantica
- Verificare che i REASON siano non vuoti
- Controllare che i riferimenti tra concetti esistano

### Validazioni

1. **Reason non vuoto** — Ogni concetto/relazione deve avere un REASON
2. **Reference integrity** — CAUSE/EFFECT devono riferire a CONCEPT esistenti
3. **Type consistency** — INPUT/OUTPUT devono usare tipi definiti
4. **Cycle detection** — Niente cicli in RELATION di tipo dipendenza

### Errori del Reasoning Engine

```python
ERRORS = {
    'E001': 'DELIMITER_MISSING',
    'E002': 'CONCEPT_UNCLOSED',
    'E003': 'REQUIRED_FIELD_MISSING',
    'E004': 'INVALID_TYPE',
    'E005': 'REASON_EMPTY',
    'E006': 'UNDEFINED_REFERENCE',
    'E007': 'CYCLE_DETECTED',
}
```

---

## Fase 4: Code Generator

### Output Python

```python
def generate_python(ast):
    output = []
    output.append("# GENERATED FROM LINGUA")
    output.append("")
    
    for node in ast:
        if isinstance(node, ConceptNode):
            output.append(f"def {node.name}({', '.join(node.input_types)}):")
            output.append(f'    """{node.reason}"""')
            output.append(f"    return {node.impl}")
            output.append("")
    
    return "\n".join(output)
```

### Output JSON

```python
def generate_json(ast):
    return json.dumps({
        'lingua_version': '1.0.0',
        'concepts': [node.__dict__ for node in ast if isinstance(node, ConceptNode)],
        'relations': [node.__dict__ for node in ast if isinstance(node, RelationNode)],
        'transforms': [node.__dict__ for node in ast if isinstance(node, TransformNode)],
        'patterns': [node.__dict__ for node in ast if isinstance(node, PatternNode)],
    }, indent=2)
```

### Output IR

```python
def generate_ir(ast):
    graph = {
        'nodes': [],
        'edges': [],
    }
    
    for node in ast:
        node_id = f"{node.__class__.__name__}_{node.name}"
        graph['nodes'].append({
            'id': node_id,
            'type': node.__class__.__name__,
            'data': node.__dict__,
        })
        
        if isinstance(node, RelationNode):
            graph['edges'].append({
                'from': f"Concept_{node.from_concept}",
                'to': f"Concept_{node.to_concept}",
                'label': node.rel_type,
            })
    
    return graph
```

---

## Struttura File del Compilatore

```
lingua/
├── src/
│   ├── __init__.py
│   ├── lexer.py          # Tokenizer
│   ├── parser.py         # Parser + AST
│   ├── reasoning.py      # Semantic validator
│   ├── generator.py      # Code generators
│   └── lingua.py         # Main entry point
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_integration.py
├── examples/
│   └── hello.lingua
├── SPEC.md
├── COMPILER.md
├── PATTERNS.md
└── EXAMPLES.md
```

---

## Interfaccia CLI

```bash
lingua compile <file.lingua> --output <python|json|ir>
lingua run <file.lingua>     # Compila e esegue in Python
lingua validate <file.lingua> # Solo validazione
lingua --version
```

---

## Flag di Compilazione

| Flag | Descrizione |
|------|-------------|
| `--output python` | Genera file Python |
| `--output json` | Genera JSON strutturato |
| `--output ir` | Genera IR (grafo) |
| `--pretty` | Output formattato |
| `--keep-comments` | Preserva commenti nell'output |
| `--strict` | Fallisce su warning |
