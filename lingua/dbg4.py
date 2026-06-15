# Test box chars
import sys
sys.path.insert(0, '.')
from lingua.lexer import Lexer

s = '\u2554\u2550\u2550\u2550\u2557'  # ╔═══╗
l = Lexer(s)
with open('dbg4_out.txt', 'w', encoding='utf-8') as f:
    f.write(f"Created lexer, pos={l.pos}, source_len={len(l.source)}\n")
    f.flush()
    try:
        tokens = l.tokenize()
        f.write(f"Got {len(tokens)} tokens\n")
        for t in tokens:
            f.write(f"  {t.type}: {repr(t.value)}\n")
    except Exception as e:
        f.write(f"Error: {type(e).__name__}: {e}\n")
        import traceback
        traceback.print_exc(file=f)