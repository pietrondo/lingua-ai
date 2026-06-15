§
╔═══╗ CONCEPT saluto
│ TYPE operazione
│ INPUT []
│ OUTPUT stringa
│ REASON "Genera un messaggio di saluto in italiano"
│ IMPL "Ciao, mondo!"
╚═══╝

╔═══╗ CONCEPT nome_completo
│ TYPE operazione
│ INPUT [nome: stringa, cognome: stringa]
│ OUTPUT stringa
│ REASON "Costruisce un nome completo da nome e cognome"
│ IMPL "f\"{nome} {cognome}\""
╚═══╝

╔═══╗ CONCEPT eta_minima
│ TYPE dato
│ OUTPUT numero
│ REASON "L'eta minima per accedere al servizio"
│ IMPL "18"
╚═══╝

╔═══╗ RELATION usa_saluto
│ FROM nome_completo
│ TO saluto
│ TYPE composizione
│ REASON "Il saluto usa il nome completo per personalizzare il messaggio"
╚═══╝

╔═══╗ TRANSFORM valuta_eta
│ CAUSE [eta]
│ EFFECT "accesso_concesso"
│ PRESERVE ["eta"]
│ CONSTRAINT "L'eta deve essere >= eta_minima"
│ MAP "eta >= int(eta_minima)"
╚═══╝

╔═══╗ PATTERN ciclo_dipendenza
│ EVIDENCE "Due concetti si riferiscono reciprocamente senza progresso"
│ CONTEXT ["dipendenza_ciclica", "nessun_termine"]
│ RESOLVE "Introdurre un terzo concetto che rompa il ciclo"
╚═══╝
§