# Minimal debug test
s = '\u2554\u2550\u2550\u2550\u2557'  # ╔═══╗
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(f"String: {repr(s)}\n")
    f.write(f"Length: {len(s)}\n")
    for i, c in enumerate(s):
        f.write(f"  [{i}] {repr(c)} ord={ord(c):04x}\n")