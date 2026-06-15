"""Test script for LINGUA."""
from lingua import parse, generate_python, generate_json

source = r"""§
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
§"""

try:
    program = parse(source)
    print(f"Parsed: {len(program.concepts)} concepts")
    print(f"Relations: {len(program.relations)}")
    print(f"Transforms: {len(program.transforms)}")
    print(f"Patterns: {len(program.patterns)}")

    print("\n--- Python Code ---")
    print(generate_python(program))
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()