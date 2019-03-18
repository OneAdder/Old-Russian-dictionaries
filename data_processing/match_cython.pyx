#cython: language_level=3, boundscheck=False
"""Этот модуль берёт оставшиеся леммы из словаря XI-XVII и добавляет их в итоговый словарь matched.json"""
__author__ = "Michael Voronov, Anna Sorokina"
__license__ = "GPLv3"

import os
import pandas
import re
from unification import compare

shit = []

x11 = []

cdef extern from "math.h":
    float roundf(float x)

def match_(avanesov):
    """Вложенный цикл по двум словарям.
    
    Переменные заранее объявлены вне цикла.
    Используется цикл while, так как он переводится в C без изменений.
    """
    avanesov_lemmas = tuple(avanesov.keys())
    cdef int number = os.getpid()
    cdef int pool_length = len(avanesov_lemmas)
    cdef int avanesov_len = len(avanesov_lemmas)
    cdef int x11_len = len(x11)
    cdef int i = 0
    cdef int j = 0
    cdef short dumm
    cdef float ready
    cdef unicode avanesov_lemma
    cdef unicode x11_lemma
    cdef unicode x11_unified
    while i < avanesov_len:
        avanesov_lemma = avanesov_lemmas[i]
        j = 0
        while j < x11_len:
            try:
                x11_lemma = x11[j]
                unified = compare(x11_lemma, avanesov_lemma)
                if unified:
                    ready = 100 - (((pool_length - i) * 100)/pool_length)
                    print(str(number) + ': %.2f' % ready + '%')
                    print(unified)
                    avanesov[avanesov_lemma]['XVII_lemma'] = x11_lemma
            except TypeError:
                dumm = 0
            j += 1
        i += 1
    return avanesov

