# LINGUA — Esempi Completi

**Versione:** 1.0.0  
**Data:** 2026-06-15

---

## 1. Hello World

```lingua
§
╔═══╗ CONCEPT saluto
│ TYPE:        operazione
│ INPUT:       []
│ OUTPUT:      stringa
│ REASON:      "produce un messaggio di test standard per validare il sistema"
│ IMPL:        "Ciao, mondo."
╚═══╝ │

╔═══╗ CONCEPT esegui
│ TYPE:        effetto
│ INPUT:       []
│ OUTPUT:      nullo
│ REASON:      "punto di ingresso principale del programma"
│ IMPL:        stampa(saluto)
╚═══╝
§
```

**Output Python:**
```python
# GENERATED FROM LINGUA

def saluto():
    """produce un messaggio di test standard per validare il sistema"""
    return "Ciao, mondo."

def esegui():
    """punto di ingresso principale del programma"""
    print(saluto())

esegui()
```

---

## 2. Calcolatrice Base

```lingua
§
╔═══╗ CONCEPT addizione
│ TYPE:        operazione
│ INPUT:       [a:numerico, b:numerico]
│ OUTPUT:      numerico
│ REASON:      "combina due numeri in un risultato aritmetico"
│ IMPL:        a + b
╚═══╝ │

╔═══╗ CONCEPT sottrazione
│ TYPE:        operazione
│ INPUT:       [a:numerico, b:numerico]
│ OUTPUT:      numerico
│ REASON:      "calcola la differenza tra due numeri"
│ IMPL:        a - b
╚═══╝ │

╔═══╗ CONCEPT moltiplicazione
│ TYPE:        operazione
│ INPUT:       [a:numerico, b:numerico]
│ OUTPUT:      numerico
│ REASON:      "calcola il prodotto di due numeri"
│ IMPL:        a * b
╚═══╝ │

╔═══╗ CONCEPT divisione
│ TYPE:        operazione
│ INPUT:       [a:numerico, b:numerico]
│ OUTPUT:      numerico
│ REASON:      "calcola il quoziente di due numeri con validazione"
│ IMPL:        a / b SE b != 0 ALTRIMENTI errore("divisione_per_zero")
╚═══╝ │

╔═══╗ TRANSFORM calcola
│ CAUSE:      [addizione, sottrazione, moltiplicazione, divisione]
│ EFFECT:     numerico
│ PRESERVE:   [precisione]
│ CONSTRAINT: "operandi devono essere numerici"
│ MAP:       Dispatch sul tipo di operazione richiesta
╚═══╝
§
```

---

## 3. Elaborazione Lista

```lingua
§
╔═══╗ CONCEPT filtro
│ TYPE:        operazione
│ INPUT:       [elementi:lista, predicato]
│ OUTPUT:      lista
│ REASON:      "estrae da una lista solo gli elementi che soddisfano il predicato"
│ IMPL:        [e per e in elementi se predicato(e)]
╚═══╝ │

╔═══╗ CONCEPT mappatura
│ TYPE:        operazione
│ INPUT:       [elementi:lista, trasformazione]
│ OUTPUT:      lista
│ REASON:      "applica una trasformazione a ogni elemento di una lista"
│ IMPL:        [trasformazione(e) per e in elementi]
╚═══╝ │

╔═══╗ CONCEPT riduzione
│ TYPE:        operazione
│ INPUT:       [elementi:lista, funzione, iniziale]
│ OUTPUT:      accumulatore
│ REASON:      "combina tutti gli elementi di una lista in un singolo valore"
│ IMPL:        riduci(funzione, iniziale, elementi)
╚═══╝ │

╔═══╗ RELATION compose_pipeline
│ FROM:   filtro
│ TO:     mappatura
│ TYPE:   trasformazione
│ REASON: "pipeline classica: filtra poi trasforma"
╚═══╝ │

╔═══╗ RELATION compose_riduci
│ FROM:   mappatura
│ TO:     riduzione
│ TYPE:   trasformazione
│ REASON: "dopo trasformazione, aggrega il risultato"
╚═══╝
§
```

---

## 4. Struttura Dato

```lingua
§
╔═══╗ CONCEPT persona
│ TYPE:        dato
│ INPUT:       []
│ OUTPUT:      struttura
│ REASON:      "rappresenta un'entità persona con dati anagrafici"
│ IMPL:        STRUTTURA
│ CAMPI:       [nome:stringa, cognome:stringa, eta:numerico, email:stringa]
╚═══╝ │

╔═══╗ CONCEPT valida_email
│ TYPE:        operazione
│ INPUT:       [email:stringa]
│ OUTPUT:      booleano
│ REASON:      "verifica che una email sia formalmente valida"
│ IMPL:        email include "@" AND email include "."
╚═══╝ │

╔═══╗ TRANSFORM crea_persona
│ CAUSE:      [nome:stringa, cognome:stringa, eta:numerico, email:stringa]
│ EFFECT:     persona
│ PRESERVE:   []
│ CONSTRAINT: "email deve essere valida"
│ MAP:        costruisci_persona_con_validazione
╚═══╝ │

╔═══╗ PATTERN validazione_ingresso
│ EVIDENCE:   "TRASFORM o CONCEPT con CONSTRAINT che verifica i parametri"
│ CONTEXT:    [input_validation, data_integrity]
│ RESOLVE:   "Estrai validazione in CONCEPT separato per riuso"
╚═══╝
§
```

---

## 5. State Machine Semplice

```lingua
§
╔═══╗ CONCEPT stato_attivo
│ TYPE:        stato
│ INPUT:       []
│ OUTPUT:      stato
│ REASON:      "rappresenta lo stato iniziale attivo della macchina"
│ IMPL:        "attivo"
╚═══╝ │

╔═══╗ CONCEPT stato_pausa
│ TYPE:        stato
│ INPUT:       []
│ OUTPUT:      stato
│ REASON:      "rappresenta lo stato di pausa temporanea"
│ IMPL:        "pausa"
╚═══╝ │

╔═══╗ CONCEPT stato_terminale
│ TYPE:        stato
│ INPUT:       []
│ OUTPUT:      stato
│ REASON:      "rappresenta lo stato finale terminale"
│ IMPL:        "terminato"
╚═══╝ │

╔═══╗ RELATION transizione_attivo_pausa
│ FROM:   stato_attivo
│ TO:     stato_pausa
│ TYPE:   trasformazione
│ REASON: "da attivo si può andare in pausa"
╚═══╝ │

╔═══╗ RELATION transizione_attivo_terminale
│ FROM:   stato_attivo
│ TO:     stato_terminale
│ TYPE:   trasformazione
│ REASON: "da attivo si può terminare direttamente"
╚═══╝ │

╔═══╗ RELATION transizione_pausa_attivo
│ FROM:   stato_pausa
│ TO:     stato_attivo
│ TYPE:   trasformazione
│ REASON: "da pausa si torna ad attivo"
╚═══╝ │

╔═══╗ CONCEPT gestore_stato
│ TYPE:        stato
│ INPUT:       [stato_corrente:stato, evento]
│ OUTPUT:      stato
│ REASON:      "gestisce le transizioni di stato in base agli eventi"
│ IMPL:        MATCH evento
              CASO "pausa" -> stato_pausa
              CASO "riprendi" -> stato_attivo
              CASO "termina" -> stato_terminale
              DEFAULT -> stato_corrente
╚═══╝
§
```

---

## 6. Query with Pipeline

```lingua
§
╔═══╗ CONCEPT utenti
│ TYPE:        dato
│ INPUT:       []
│ OUTPUT:      lista
│ REASON:      "dataset degli utenti registrati"
│ IMPL:        [
                  {nome: "Alice", eta: 30, citta: "Roma"},
                  {nome: "Bob", eta: 25, citta: "Milano"},
                  {nome: "Charlie", eta: 35, citta: "Roma"}
                ]
╚═══╝ │

╔═══╗ CONCEPT filtra_per_citta
│ TYPE:        operazione
│ INPUT:       [utenti:lista, citta:stringa]
│ OUTPUT:      lista
│ REASON:      "filtra utenti per città di residenza"
│ IMPL:        filtro(utenti, lambda u: u.citta == citta)
╚═══╝ │

╔═══╗ CONCEPT media_eta
│ TYPE:        operazione
│ INPUT:       [utenti:lista]
│ OUTPUT:      numerico
│ REASON:      "calcola l'età media di una lista di utenti"
│ IMPL:        riduzione(utenti, lambda acc, u: acc + u.eta, 0) / lunghezza(utenti)
╚═══╝ │

╔═══╗ PATTERN pipeline_analisi
│ EVIDENCE:   "sequenza di trasformazioni dove output di una è input della successiva"
│ CONTEXT:    [data_processing, etl, analytics]
│ RESOLVE:   "Compatta in un singolo CONCEPT pipeline con REASON che descrive l'obiettivo finale"
╚═══╝
§
```

---

## 7. Error Handling

```lingua
§
╔═══╗ CONCEPT risultato
│ TYPE:        dato
│ INPUT:       []
│ OUTPUT:      struttura
│ REASON:      "tipo che rappresenta un risultato che può essere successo o errore"
│ IMPL:        STRUTTURA
│ CAMPI:       [successo:booleano, valore, errore:stringa]
╚═══╝ │

╔═══╗ CONCEPT successo
│ TYPE:        operazione
│ INPUT:       [valore]
│ OUTPUT:      risultato
│ REASON:      "costruisce un risultato di successo"
│ IMPL:        {successo: vero, valore: valore, errore: nullo}
╚═══╝ │

╔═══╗ CONCEPT fallimento
│ TYPE:        operazione
│ INPUT:       [errore:stringa]
│ OUTPUT:      risultato
│ REASON:      "costruisce un risultato di errore"
│ IMPL:        {successo: falso, valore: nullo, errore: errore}
╚═══╝ │

╔═══╗ CONCEPT gestisci_risultato
│ TYPE:        meta
│ INPUT:       [risultato:risultato, successo_fn, errore_fn]
│ OUTPUT:      qualunque
│ REASON:      "applica la funzione appropriata basata sul successo o fallimento"
│ IMPL:        successo_fn(risultato.valore) SE risultato.successo ALTRIMENTI errore_fn(risultato.errore)
╚═══╝
§
```

---

## 8. Esempio Completo: Todo List

```lingua
§
╔═══╗ CONCEPT todo_item
│ TYPE:        dato
│ INPUT:       []
│ OUTPUT:      struttura
│ REASON:      "rappresenta un singolo item della todo list"
│ IMPL:        STRUTTURA
│ CAMPI:       [id:numerico, titolo:stringa, completato:booleano]
╚═══╝ │

╔═══╗ CONCEPT lista_todo
│ TYPE:        stato
│ INPUT:       []
│ OUTPUT:      lista
│ REASON:      "mantiene la collezione di tutti i todo items"
│ IMPL:        []
╚═══╝ │

╔═══╗ CONCEPT aggiungi_todo
│ TYPE:        effetto
│ INPUT:       [lista:lista_todo, titolo:stringa]
│ OUTPUT:      lista_todo
│ REASON:      "aggiunge un nuovo item alla lista"
│ IMPL:        lista + [{id: prossimo_id(lista), titolo: titolo, completato: falso}]
╚═══╝ │

╔═══╗ CONCEPT completa_todo
│ TYPE:        effetto
│ INPUT:       [lista:lista_todo, id:numerico]
│ OUTPUT:      lista_todo
│ REASON:      "segn un item come completato"
│ IMPL:        segna_completato(lista, id)
╚═══╝ │

╔═══╗ CONCEPT rimuovi_completati
│ TYPE:        effetto
│ INPUT:       [lista:lista_todo]
│ OUTPUT:      lista_todo
│ REASON:      "rimuove tutti gli item già completati dalla lista"
│ IMPL:        filtro(lista, lambda t: NOT t.completato)
╚═══╝ │

╔═══╗ RELATION gestisce
│ FROM:   lista_todo
│ TO:     todo_item
│ TYPE:   composizione
│ REASON: "la lista contiene e gestisce gli item"
╚═══╝
§
```

---

## Output JSON di un Esempio

Input: Hello World

```json
{
  "lingua_version": "1.0.0",
  "concepts": [
    {
      "name": "saluto",
      "type": "operazione",
      "input_types": [],
      "output_type": "stringa",
      "reason": "produce un messaggio di test standard per validare il sistema",
      "impl": "\"Ciao, mondo.\""
    }
  ],
  "relations": [],
  "transforms": [],
  "patterns": []
}
```