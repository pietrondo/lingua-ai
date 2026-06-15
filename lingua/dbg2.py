# Test Lexer with box characters
import sys
sys.path.insert(0, '.')
from lingua.lexer import Lexer, TokenType

s = '\u2554\u2550\u2550\u2550\u2557'  # ╔═══╗
with open('lex_out.txt', 'w', encoding='utf-8') as f:
    f.write(f"Input: {repr(s)}\n")
    f.write(f"Input len: {len(s)}\n")
    l = Lexer(s)
    f.write(f"Lexer created, pos={l.pos}, source_len={len(l.source)}\n")
    try:
        tokens = l.tokenize()
        f.write(f"Success: {len(tokens)} tokens\n")
        for t in tokens:
            f.write(f"  {t.type} = {repr(t.value)}\n")
    except Exception as e:
        f.write(f"Error: {type(e).__name__}: {e}\n")
        import traceback
        traceback.print_exc(file=f)