"""Show line 15 of saluto.lua"""
with open('examples/saluto.lua', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('line15_out.txt', 'w', encoding='utf-8') as f:
    for i, line in enumerate(lines[:20], 1):
        f.write(f"Line {i}: {repr(line)}\n")
print("done")