import json
import pandas
import itertools

from multiprocessing import Pool

from unification import unify

with open('avanesov2.json', 'r', encoding='utf-8') as f:
    avanesov = json.loads(f.read())

shit = pandas.read_csv('wordlist_linked.csv', delimiter=',', header=0)

x11 = list(shit.MainLemma)
#print(x11[0:20])

lengt = len(avanesov)
print('Total:')
print(lengt)


def splitDict(d):
    n = len(d) // 2
    i = iter(d.items())

    d1 = dict(itertools.islice(i, n))
    d2 = dict(i)
    return d1, d2

avanesov1, avanesov2 = splitDict(avanesov)
#print(len(avanesov1))
#print(len(avanesov2))

r = 0
bingos = 0

def match_(avanesov):
    global x11
    global r
    global bingos
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
    return avanesov

pool = Pool(processes=2)
matched1 = pool.map(match_, (avanesov1,))
matched2 = pool.map(match_, (avanesov2,))
matched = {**matched1, **matched2}

print('!bingos!')
print(bingos)
print('!bingos!')

for x11_lemma in x11:
    matched[avanesov_lemma]['XVII_lemma'] = x11_lemma
    matched[avanesov_lemma]['bingo'] = False

with open('matched.json', 'w') as f:
    json.dump(matched, f, indent=4, ensure_ascii=False)

