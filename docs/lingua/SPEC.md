# LINGUA — Specifica del Linguaggio

**Versione:** 1.0.0  
**Data:** 2026-06-15  
**Stato:** Design completato

---

## Filosofia

LINGUA (Linguaggio Intelligente Guidato Unicamente per Agenti) è un linguaggio di programmazione dove la struttura è pensata per essere decomponibile da un LLM in modo naturale, ma che presenta agli umani una facciata aliena, inconsistente a prima vista, e deliberatamente non familiare.

Ogni costrutto LINGUA include metadati espliciti sul "perché" del codice, non solo sul "cosa". Questo permette a un AI di:
- Ragionare sul codice come su una knowledge graph
- Identificare pattern ricorrenti
- Generare codice coerente con l'intento originale
- Spiegare le decisioni architetturali

---

## Struttura Lessicale

### Delimitatori Globali

```
§ [codice] §
```

Tutto il codice LINGUA deve essere racchiuso tra `§` di apertura e chiusura.

### Separatori di Statement

```
│   (pipe singolo) — separatore di statement su linea singola
```

### Commenti

```
◇ Questo è un commento visibile solo all'AI
```

I commenti iniziano con `◇` e sono ignorati dal compilatore ma preservati nell'output JSON per diagnostica AI.

### Delimitatori di Blocco

```
╔═══╗   — delimitatore di apertura concetto
╚═══╝   — delimitatore di chiusura concetto
```

---

## Concetti Core

### 1. CONCEPT

Definisce un'entità computazionale.

**Sintassi:**
```
╔═══╗ CONCEPT nome_entità
│ TYPE:        tipologia
│ INPUT:       [arg1:TIPO, arg2:TIPO, ...]
│ OUTPUT:      tipo_output
│ REASON:      "perché esiste questo concetto"
│ IMPL:        corpo
╚═══╝
```

**TYPE disponibili:**
- `operazione` — funzione pura
- `dato` — dato strutturato
- `stato` — entità con memoria
- `effetto` — operazione con side-effect
- `meta` — concetto che descrive altri concetti

**Esempio:**
```
╔═══╗ CONCEPT addizione
│ TYPE:        operazione
│ INPUT:       [a:numerico, b:numerico]
│ OUTPUT:      numerico
│ REASON:      "combina due numeri in un risultato"
│ IMPL:        a + b
╚═══╝
```

---

### 2. RELATION

Definisce una relazione tra concetti.

**Sintassi:**
```
╔═══╗ RELATION nome_relazione
│ FROM:   concetto_a
│ TO:     concetto_b
│ TYPE:   tipologia_relazione
│ REASON: "perché esiste questa relazione"
╚═══╝
```

**TYPE disponibili:**
- `dipendenza` — B dipende da A
- `composizione` — B è parte di A
- `ereditarietà` — B estende A
- `trasformazione` — B è trasformazione di A
- `associazione` — B è associato a A senza dipendenza

---

### 3. TRANSFORM

Definisce una trasformazione esplicita tra concetti.

**Sintassi:**
```
╔═══╗ TRANSFORM nome_trasformazione
│ CAUSE:      concetto_input
│ EFFECT:     concetto_output
│ PRESERVE:   [proprietà_da_mantenere]
│ CONSTRAINT: "vincolo formale"
│ MAP:        regola_di_mappatura
╚═══╝
```

---

### 4. PATTERN

Definisce un pattern riconoscibile dall'AI.

**Sintassi:**
```
╔═══╗ PATTERN nome_pattern
│ EVIDENCE:   "come si manifesta"
│ CONTEXT:    [situazioni_dove_appare]
│ RESOLVE:   "come risolvere"
╚═══╝
```

---

## Sistema di Tipi

### Tipi Primitivi

| LINGUA | Python      | JavaScript |
|--------|-------------|------------|
| `numerico` | `int/float` | `number` |
| `stringa` | `str` | `string` |
| `booleano` | `bool` | `boolean` |
| `lista` | `list` | `array` |
| `mappa` | `dict` | `object` |
| `nullo` | `None` | `null` |

### Tipi Strutturati

```
STRUTTURA nome_struttura
│ CAMPI: [campo1:tipo1, campo2:tipo2]
╚═══╝
```

---

## Espressioni

### Operatori Aritmetici

| Operatore | Significato |
|-----------|-------------|
| `+` | addizione |
| `-` | sottrazione |
| `*` | moltiplicazione |
| `/` | divisione |
| `%` | modulo |
| `**` | potenza |

### Operatori di Confronto

| Operatore | Significato |
|-----------|-------------|
| `==` | uguaglianza |
| `!=` | disuguaglianza |
| `<` | minore |
| `>` | maggiore |
| `<=` | minore uguale |
| `>=` | maggiore uguale |

### Operatori Logici

| Operatore | Significato |
|-----------|-------------|
| `AND` | congiunzione |
| `OR` | disgiunzione |
| `NOT` | negazione |

---

## Strutture di Controllo

### Condizionale

```
╔═══╗ IF condizione
│ THEN:   statement_o_concetto
│ ELSE:   statement_o_concetto_opzionale
╚═══╝
```

### Iterazione

```
╔═══╗ REPEAT n_volte
│ DO:    statement_o_concetto
╚═══╝
```

```
╔═══╗ WHILE condizione
│ DO:    statement_o_concetto
╚═══╝
```

### Match

```
╔═══╗ MATCH valore
│ CASE:  pattern1 -> risultato1
│ CASE:  pattern2 -> risultato2
│ DEFAULT: risultato_default
╚═══╝
```

---

## Regole di Parsing

1. **Indentazione:** non significativa (usa `│` per separatori)
2. **Maiuscole/minuscole:** significative per keywords
3. **Stringhe:** sempre tra doppi apici `"`
4. **Liste:** sempre tra parentesi quadre `[...]`
5. **Commenti:** sempre su linea singola, iniziano con `◇`

---

## Output del Compilatore

### JSON Strutturato

```json
{
  "lingua_version": "1.0.0",
  "concepts": [...],
  "relations": [...],
  "transforms": [...],
  "patterns": [...],
  "ast": {...}
}
```

### Python

Codice Python equivalente, preservando i commenti REASON come docstring.

### IR (Intermediate Representation)

Grafo JSON della computazione per analisi AI.

---

## Errori

### Codici di Errore

| Codice | Significato |
|--------|-------------|
| `E001` | Delimitatore mancante |
| `E002` | CONCEPT non chiuso |
| `E003` | Campo obbligatorio mancante |
| `E004` | Tipo non valido |
| `E005` | REASON vuoto |

---

## Esempio Completo

```
§
╔═══╗ CONCEPT saluto
│ TYPE:        operazione
│ INPUT:       []
│ OUTPUT:      stringa
│ REASON:      "produce un messaggio di test standard"
│ IMPL:        "Ciao, mondo."
╚═══╝ │

╔═══╗ TRANSFORM esegui_saluto
│ CAUSE:      saluto
│ EFFECT:     stringa
│ PRESERVE:   []
│ CONSTRAINT: "nessuna"
│ MAP:        identità
╚═══╝
§
```
