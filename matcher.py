import json
import pandas
from unification import unify


with open('avanesov2.json', 'r', encoding='utf-8') as f:
    avanesov = json.loads(f.read())

shit = pandas.read_csv('wordlist_linked.csv', delimiter=',', header=0)

x11 = list(shit.MainLemma)
#print(x11[0:20])

lengt = len(avanesov.keys())
print('Total:')
print(lengt)

bingos = 0
r = 0
for avanesov_lemma in avanesov:
    for x11_lemma in x11:
        x11_unified = unify(x11_lemma)
        if x11_unified == avanesov_lemma:
            print()
            print('Ready:')
            print(100 - (((lengt - r) * 100)/lengt))
            print(x11_unified)
            i = x11.index(x11_lemma)
            x11.pop(i)
            avanesov[avanesov_lemma]['XVII_lemma'] = x11_lemma
            avanesov[avanesov_lemma]['bingo'] = True
            bingos += 1
        else:
            avanesov[avanesov_lemma]['bingo'] = False
    r += 1

print('!bingos!')
print(bingos)
print('!bingos!')

for x11_lemma in x11:
    avanesov[avanesov_lemma]['XVII_lemma'] = x11_lemma
    avanesov[avanesov_lemma]['bingo'] = False

with open('matched.json', 'w') as f:
    json.dump(avanesov, f, indent=4, ensure_ascii=False)

