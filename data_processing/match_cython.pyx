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
    avanesov_lemmas = tuple(avanesov.keys())
    cdef int number = os.getpid()
    cdef int pool_length = len(avanesov_lemmas)
    cdef int avanesov_len = len(avanesov_lemmas)
    cdef int x11_len = len(x11)
    cdef int i = 0
    cdef int j = 0
    while i < avanesov_len:
        avanesov_lemma = avanesov_lemmas[i]
        j = 0
        while j < x11_len:
            x11_lemma = x11[j]
            x11_unified = unify(x11_lemma)
            if x11_unified == avanesov_lemma:
                ready = round(100 - (((pool_length - i) * 100)/pool_length), 2)
                print(str(number) + ': ' + str(ready) + '%')
                print(x11_unified)
                avanesov[avanesov_lemma]['XVII_lemma'] = x11_lemma
            j += 1
        i += 1
    return avanesov

