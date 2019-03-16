#cython: language_level=3, boundscheck=False

__author__ = "Michael Voronov, Anna Sorokina"
__license__ = "GPLv3"

import os
import pandas
import re
from unification import unify

shit = pandas.read_csv('wordlist_linked.csv', delimiter=',', header=0)

x11 = list(shit.MainLemma)

def match_(avanesov):
    """Вложенный цикл по двум словарям."""
    global x11
    cdef int number = os.getpid()
    cdef int r = 0
    cdef int pool_length = len(avanesov)
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

