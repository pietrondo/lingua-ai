"""Test parser with saluto.lua"""
from lingua.lexer import Lexer
from lingua.parser import Parser

with open('examples/saluto.lua', 'r', encoding='utf-8') as f:
    source = f.read()

l = Lexer(source)
tokens = l.tokenize()
print(f"Lexer: {len(tokens)} tokens OK")

p = Parser(tokens)
try:
    ast = p.parse()
    with open('ast_out.txt', 'w', encoding='utf-8') as f:
        f.write(f"SUCCESS: concepts={len(ast.concepts)}, relations={len(ast.relations)}, transforms={len(ast.transforms)}, patterns={len(ast.patterns)}\n\n")
        for i, c in enumerate(ast.concepts):
            f.write(f"Concept {i}: {c}\n")
        for i, r in enumerate(ast.relations):
            f.write(f"Relation {i}: {r}\n")
        for i, t in enumerate(ast.transforms):
            f.write(f"Transform {i}: {t}\n")
        for i, p in enumerate(ast.patterns):
            f.write(f"Pattern {i}: {p}\n")
    print(f"Parser: {len(ast.concepts)} concepts OK - written to ast_out.txt")
except Exception as e:
    print(f"Parser error: {e}")
    import traceback
    traceback.print_exc()