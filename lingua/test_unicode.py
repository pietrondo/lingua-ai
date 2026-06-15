s = '\u2554\u2550\u2550\u2550\u2557'
pat = '\u2554\u2550\u2550\u2550\u2557'
with open('test_unicode.txt', 'w', encoding='utf-8') as f:
    f.write(f'len={len(s)}\n')
    f.write(f'pat_len={len(pat)}\n')
    f.write(f's.startswith(pat)={s.startswith(pat)}\n')
    f.write(f's[0:1]={repr(s[0:1])}, isalpha={s[0:1].isalpha()}\n')
    f.write(f'source[0:5]={repr(s[0:5])}\n')
    f.write(f'source[0:5].startswith(pat)={s[0:5].startswith(pat)}\n')
    f.write(f'at pos=0: source.startswith(pat)={s.startswith(pat)}\n')
print('done')