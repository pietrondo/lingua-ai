from lingua.lexer import Lexer

source = """§
╔═══╗ CONCEPT saluto
│ TYPE operazione
│ INPUT []
│ OUTPUT stringa
│ REASON "Genera un messaggio di saluto"
│ IMPL "Ciao, mondo!"
╚═══╝
§"""
for tok in Lexer(source).tokenize():
    val_repr = repr(tok.value).encode('ascii', 'backslashreplace').decode('ascii')
    print(f'{tok.type.name:20s} {val_repr:30s} line={tok.line} col={tok.column}')