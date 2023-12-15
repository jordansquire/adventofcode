from pathlib import Path
from collections import defaultdict


def ascii_hash(string: str):
    res = 0
    for c in string:
        res = ((res + ord(c)) * 17) % 256
    return res


def solutions():
    data = Path("input.txt").read_text().strip().split(',')
    extract = lambda s: s.split('-')[0] if '-' in s else s.split('=')[0] if '=' in s else ''
    hashmap, seen = defaultdict(list), defaultdict(set)
    sol1, sol2 = 0, 0
    for s in data:
        sol1 += ascii_hash(s)
        h = ascii_hash(extract(s))  # key
        if s.endswith("-"):  # deletion
            label = s[:-1]
            if label in seen[h]:  # deletion only happens if label in values of given key
                for i, v in enumerate(hashmap[h]):  # find the value, delete it, update `seen`
                    if v.split()[0] == label:
                        seen[h].remove(label)
                        del hashmap[h][i];
                        break
        else:  # not deletion -> addition
            label, value = s.split("=")
            if label in seen[h]:  # Label is present in values
                for i, v in enumerate(hashmap[h]):  # update value
                    if v.split()[0] == label:
                        hashmap[h][i] = f"{label} {value}";
                        break
            else:
                seen[h].add(label);
                hashmap[h].append(f"{label} {value}")  # not yet present, add it

    for k in hashmap:
        for i, v in enumerate(hashmap[k]):
            sol2 += (k + 1) * (i + 1) * int(v.split()[1])


    print(sol2)

solutions()
