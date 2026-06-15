# LINGUA — Pattern AI-Riconoscibili

**Versione:** 1.0.0  
**Data:** 2026-06-15

---

## Introduzione

I PATTERN in LINGUA permettono a un AI di riconoscere situazioni ricorrenti nel codice. Ogni pattern include EVIDENCE (come si manifesta), CONTEXT (dove appare), e RESOLVE (come risolvere).

---

## Pattern Strutturali

### PATTERN pipeline_sequenziale

**EVIDENCE:** `TRASFORM` con CAUSE che è EFFECT di un altro TRANSFORM  
**CONTEXT:** `[elaborazione_dati, flusso_lavorazione, catena_operatori]`  
**RESOLVE:** "Compattare in un singolo CONCEPT con REASON che spiega l'intera pipeline"

```
╔═══╗ PATTERN pipeline_sequenziale
│ EVIDENCE:   "TRASFORM A ha CAUSE -> EFFECT di TRASFORM B"
│ CONTEXT:    [elaborazione_dati, catena_operatori]
│ RESOLVE:   "Unificare in un singolo CONCEPT che incapsula l'intera sequenza"
╚═══╝
```

---

### PATTERN funzione_ridondante

**EVIDENCE:** CONCEPT con IMPL che è solo una chiamata a un altro CONCEPT  
**CONTEXT:** `[wrappers, adattatori, bridge]`  
**RESOLVE:** "Eliminare il layer di astrazione superfluo"

---

### PATTERN dato_spoglio

**EVIDENCE:** CONCEPT TYPE:dato senza CAMPI definiti  
**CONTEXT:** `[strutture_minime,голый_данные]`  
**RESOLVE:** "Avvolgere in una STRUTTURA con invarianti esplicite"

---

### PATTERN relazione_non_utilizzata

**EVIDENCE:** RELATION mai referenziata in nessun TRANSFORM  
**CONTEXT:** `[dead_code, architettura_legacy]`  
**RESOLVE:** "Rimuovere o documentare perché è ancora presente"

---

## Pattern Semantici

### PATTERN scopo_vago

**EVIDENCE:** REASON con meno di 3 parole o generico ("fa cose", "elabora")  
**CONTEXT:** `[documentazione, manutenzione]`  
**RESOLVE:** "Scomporre in REASON specifici per ogni sottocomponente"

---

### PATTERN ciclo_dipendenza

**EVIDENCE:** RELATION TYPE:dipendenza forma un ciclo A -> B -> C -> A  
**CONTEXT:** `[architettura, refactoring]`  
**RESOLVE:** "Introdurre un'interfaccia comune o invertire una dipendenza"

---

### PATTERN trasformazione_vuota

**EVIDENCE:** TRANSFORM con MAP: identità e PRESERVE contiene tutto  
**CONTEXT:** `[pass-through, proxy]`  
**RESOLVE:** "Rimuovere e usare il concetto input direttamente"

---

### PATTERN effetto_collaterale

**EVIDENCE:** CONCEPT TYPE:operazione con IMPL che modifica stato esterno  
**CONTEXT:** `[side_effects, impure_functions]`  
**RESOLVE:** "Separare in CONCEPT TYPE:effetto con IMPL esplicito e documentato"

---

## Pattern di Qualità

### PATTERN testabilità_bassa

**EVIDENCE:** CONCEPT con dipendenze implicite (nessun INPUT definito ma usa altri CONCEPT)  
**CONTEXT:** `[testing, dependency_injection]`  
**RESOLVE:** "Aggiungere INPUT espliciti per ogni dipendenza"

---

### PATTERN nome_non_descrittivo

**EVIDENCE:** CONCEPT/RELATION con nome generico (data, stuff, thing)  
**CONTEXT:** `[naming, code_review]`  
**RESOLVE:** "Rinominare con verbo+nome che descrive lo scopo"

---

### PATTERN documento_assente

**EVIDENCE:** CONCEPT senza REASON o REASON: ""  
**CONTEXT:** `[documentazione, onboarding]`  
**RESOLVE:** "Aggiungere REASON che spiega il perché dell'esistenza"

---

### PATTERN tipo_implicito

**EVIDENCE:** CAMPI senza tipo specificato o tipo generico  
**CONTEXT:** `[type_safety, debugging]`  
**RESOLVE:** "Specificare tipi concreti per ogni campo"

---

## Pattern Architetturali

### PATTERN facciata_esterna

**EVIDENCE:** RELATION TYPE:associazione verso un sistema esterno  
**CONTEXT:** `[integrazione, legacy_code]`  
**RESOLVE:** "Creare un CONCEPT TYPE:meta che documenti il contract"

---

### PATTERN singleton_implicito

**EVIDENCE:** CONCEPT TYPE:stato con una sola istanza logica  
**CONTEXT:** `[global_state, configurazione]`  
**RESOLVE:** "Esplicitare con PATTERN singleton e documentare lifecycle"

---

### PATTERN strategia_non_template

**EVIDENCE:** CONCEPT con IF/SWITCH su parametri invece di RELATION tipo ereditarietà  
**CONTEXT:** `[design_patterns, extensibility]`  
**RESOLVE:** "Sostituire con RELATION TYPE:ereditarietà e CONCEPT figli specializzati"

---

## Pattern di Optimizzazione

### PATTERN ripetizione_calcolo

**EVIDENCE:** Stesso CONCEPT chiamato multipli volte con stessi INPUT  
**CONTEXT:** `[performance, memoization]`  
**RESOLVE:** "Introdurre cache esplicita o trasformare in pipeline"

---

### PATTERN trasformazione_scomponibile

**EVIDENCE:** TRANSFORM con MAP complessa che può essere spezzata in sequence  
**CONTEXT:** `[modularità, riuso]`  
**RESOLVE:** "Scomporre in TRANSFORM atomici composti"

---

## Guida per l'AI

Quando analizzi codice LINGUA, usa questa matrice:

| Se vedi... | Considera... |
|------------|-------------|
| REASON breve/vago | `scopo_vago` |
| TRANSFORM con MAP:identità | `trasformazione_vuota` |
| RELATION in ciclo | `ciclo_dipendenza` |
| CONCEPT senza REASON | `documento_assente` |
| TYPE:operazione con side-effect | `effetto_collaterale` |
| CONCEPT ripetuto con stessi INPUT | `ripetizione_calcolo` |
| RELATION mai usata | `relazione_non_utilizzata` |

---

## Esempio di Analisi

Input LINGUA:
```
§
╔═══╗ CONCEPT elaboratore
│ TYPE:        operazione
│ INPUT:       [dati]
│ OUTPUT:      risultato
│ REASON:      "elabora"
│ IMPL:        dati * 2
╚═══╝ │

╔═══╗ RELATION va_dopo
│ FROM:   calcolatore
│ TO:     visualizzatore
│ TYPE:   dipendenza
│ REASON: ""
╚═══╝
§
```

Analisi AI:
- `elaboratore`: REASON troppo vago → `scopo_vago`
- `va_dopo`: REASON vuoto → `documento_assente`
- `calcolatore` e `visualizzatore`: referenziati ma non definiti → `E006: UNDEFINED_REFERENCE`
