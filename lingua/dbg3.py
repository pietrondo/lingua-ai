# Minimal test
import sys
sys.path.insert(0, '.')
from lingua.lexer import Lexer

s = 'A'  # Just ASCII first
l = Lexer(s)
print("Created lexer for 'A'")
tokens = l.tokenize()
print(f"Got {len(tokens)} tokens")