# Read saluto.lua and test lexer
import sys
sys.path.insert(0, '.')
from lingua.lexer import Lexer

with open('examples/saluto.lua', 'r', encoding='utf-8') as f:
    text = f.read()

with open('saluto_info.txt', 'w', encoding='utf-8') as f:
    f.write(f"File len: {len(text)}\n")
    f.write(f"First 200 chars:\n")
    f.write(repr(text[:200]) + "\n")
    f.write("\nBox chars in first 200:\n")
    for i, c in enumerate(text[:200]):
        if ord(c) > 127:
            f.write(f"  [{i}] {repr(c)} ord={ord(c):04x}\n")

    f.write("\nLexer test:\n")
    l = Lexer(text)
    try:
        tokens = l.tokenize()
        f.write(f"Success: {len(tokens)} tokens\n")
        for t in tokens[:20]:
            f.write(f"  {t.type}: {repr(t.value)}\n")
    except Exception as e:
        f.write(f"Error: {type(e).__name__}: {e}\n")
        import traceback
        traceback.print_exc(file=f)