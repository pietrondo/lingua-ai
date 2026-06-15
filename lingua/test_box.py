# Minimal debug test
s = '\u2554\u2550\u2550\u2550\u2557'  # ╔═══╗
print(f"String: {repr(s)}")
print(f"Length: {len(s)}")
for i, c in enumerate(s):
    print(f"  [{i}] {repr(c)} ord={ord(c):04x}")