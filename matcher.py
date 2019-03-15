import json
import pandas
import itertools
import random

from multiprocessing import Pool

from unification import unify

#a = {'a': 'b'}
#b = {'c': 'd'}
#c = {'e': 'f'}
#d = {'g': 'h'}
#print({**a, **b, **c, **d})

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

avanesov1, avanesov3 = splitDict(avanesov)
#print(len(avanesov1))
#print(len(avanesov2))

avanesov1, avanesov2 = splitDict(avanesov1)
avanesov3, avanesov4 = splitDict(avanesov3)

bingos = 0

def match_(avanesov):
    global x11
    global bingos
    #Два аргумента сложно передавать, поэтому такой колхоз
    number = random.randint(0, 20)
    r = 0
    pool_length = len(avanesov)
    for avanesov_lemma in avanesov:
        for x11_lemma in x11:
            x11_unified = unify(x11_lemma)
            if x11_unified == avanesov_lemma:
                ready = 100 - (((pool_length - r) * 100)/pool_length)
                print(str(number) + ': ' + str(ready))
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

pool = Pool(processes=4)
matched1, matched2, matched3, matched4 = pool.map(match_, (avanesov1, avanesov2, avanesov3, avanesov4))
matched = {**matched1, **matched2, **matched3, **matched4}

print('!bingos!')
print(bingos)
print('!bingos!')

for x11_lemma in x11:
    matched[avanesov_lemma]['XVII_lemma'] = x11_lemma
    matched[avanesov_lemma]['bingo'] = False

with open('matched.json', 'w') as f:
    json.dump(matched, f, indent=4, ensure_ascii=False)

