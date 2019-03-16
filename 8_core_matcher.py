import json
import pandas
import itertools
import random

from multiprocessing import Pool
import os

from unification import unify

CPU_CORES = 8

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

avanesov11, avanesov12 = splitDict(avanesov1)
avanesov21, avanesov22 = splitDict(avanesov2)
avanesov31, avanesov32 = splitDict(avanesov3)
avanesov41, avanesov42 = splitDict(avanesov4)


def match_(avanesov):
    global x11
    #Два аргумента сложно передавать, поэтому такой колхоз
    number = os.getpid()
    r = 0
    pool_length = len(avanesov)
    for avanesov_lemma in avanesov:
        for x11_lemma in x11:
            x11_unified = unify(x11_lemma)
            if x11_unified == avanesov_lemma:
                ready = 100 - (((pool_length - r) * 100)/pool_length)
                print(str(number) + ': ' + str(ready))
                print(x11_unified)
                avanesov[avanesov_lemma]['XVII_lemma'] = x11_lemma
        r += 1
    return avanesov

pool = Pool(processes=CPU_CORES)
matched1, matched2, matched3, matched4, matched5, matched6, matched7, matched8 = pool.map(match_, (avanesov11, avanesov12,
                                                                                                   avanesov21, avanesov22,
                                                                                                   avanesov31, avanesov32,
                                                                                                   avanesov41, avanesov42))
matched = {**matched1, **matched2, **matched3, **matched4, **matched5, **matched6, **matched7, **matched8}

with open('prematched.json', 'w') as f:
    json.dump(matched, f, indent=4, ensure_ascii=False)


 
