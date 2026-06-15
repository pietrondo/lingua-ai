"""Quick test to find all lexer errors."""
from lingua.lexer import Lexer, LexerError

with open('examples/saluto.lua', 'r', encoding='utf-8') as f:
    source = f.read()

l = Lexer(source)
try:
    tokens = l.tokenize()
    with open('tokens_out.txt', 'w', encoding='utf-8') as f:
        f.write(f"SUCCESS: {len(tokens)} tokens\n\n")
        for i, t in enumerate(tokens):
            f.write(f"  [{i}] {t.type.name}: {repr(t.value)}\n")
    print(f"SUCCESS: {len(tokens)} tokens written to tokens_out.txt")
except LexerError as e:
    print(f"LexerError: {e}")