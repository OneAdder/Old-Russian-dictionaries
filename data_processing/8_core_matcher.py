import json
import pandas
import itertools
import random
import pyximport; pyximport.install()
import match_cython

from multiprocessing import Pool
import os

CPU_CORES = 8

with open('avanesov2.json', 'r', encoding='utf-8') as f:
    avanesov = json.loads(f.read())

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

avanesov1, avanesov2 = splitDict(avanesov1)
avanesov3, avanesov4 = splitDict(avanesov3)

avanesov11, avanesov12 = splitDict(avanesov1)
avanesov21, avanesov22 = splitDict(avanesov2)
avanesov31, avanesov32 = splitDict(avanesov3)
avanesov41, avanesov42 = splitDict(avanesov4)


match_ = match_cython.match_

pool = Pool(processes=CPU_CORES)
matched1, matched2, matched3, matched4, matched5, matched6, matched7, matched8 = pool.map(match_, (avanesov11, avanesov12,
                                                                                                   avanesov21, avanesov22,
                                                                                                   avanesov31, avanesov32,
                                                                                                   avanesov41, avanesov42))
matched = {**matched1, **matched2, **matched3, **matched4, **matched5, **matched6, **matched7, **matched8}

with open('prematched.json', 'w') as f:
    json.dump(matched, f, indent=4, ensure_ascii=False)


 
