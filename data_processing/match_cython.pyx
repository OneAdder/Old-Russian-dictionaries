#cython: language_level=3, boundscheck=False
"""Этот модуль берёт оставшиеся леммы из словаря XI-XVII и добавляет их в итоговый словарь matched.json"""
__author__ = "Michael Voronov, Anna Sorokina"
__license__ = "GPLv3"

import os
import pandas
import re
from unification import all_options

x11 = []
x11_index = []
    
def match_(avanesov):
    """Вложенный цикл по двум словарям.
    
    Переменные заранее объявлены вне цикла.
    Используется цикл while, так как он переводится в C без изменений.
    """
    avanesov_lemmas = tuple(avanesov.keys())
    cdef int number = os.getpid()
    cdef int pool_length = len(avanesov_lemmas)
    cdef int avanesov_len = len(avanesov_lemmas)
    cdef long int x11_len = len(x11)
    
    cdef unicode avanesov_lemma
    cdef unicode x11_lemma
    
    cdef list unified = []
    cdef list unified_index = []
    
    cdef long int x = 0
    cdef long int i = 0
    cdef long int j = 0
    cdef short y = 20
    
    cdef short dumm
    
    cdef list new_x11 = []
    cdef list new_x11_index = []
    
    print('Preparing data...\r', end='')
    while x < x11_len:
        if isinstance(x11[x], str):
            unified.append(all_options(x11[x]))
            new_x11.append(x11[x])
            if isinstance(x11_index[x], str):
                unified_index.append(all_options(x11_index[x]))
                new_x11_index.append(x11_index[x])
            else:
                unified_index.append(tuple())
                new_x11_index.append('')
        else:
            if isinstance(x11_index[x], str):
                unified.append(all_options(x11_index[x]))
                new_x11.append(x11_index[x])
                unified_index.append(all_options(x11_index[x]))
                new_x11_index.append(x11_index[x])
            else:
                unified_index.append(tuple())
                new_x11_index.append('')
            
        x += 1
    
    print('Finished, starting matching.\r', end='')
    print('                            \r', end='')
    
    cdef long int new_x11_len = len(new_x11)
    
    while i < avanesov_len:
        avanesov_lemma = avanesov_lemmas[i]
        j = 0
        while j < new_x11_len:
            x11_lemma = new_x11[j]
            unified_x11 = unified[j]
            if avanesov_lemma in unified[j] or avanesov_lemma in unified_index[j]:
                ready = 100 - (((pool_length - i) * 100)/pool_length)
                if y < 50:
                    y += 1
                else:
                    print(str(number) + ': %.2f' % ready + '%\r', end='')
                    y = 0
                #print(avanesov_lemma)
                avanesov[avanesov_lemma]['XVII_lemma'] = x11_lemma
                avanesov[avanesov_lemma]['XVII_lemma_index'] = new_x11_index[j]
            j += 1
        i += 1
    return avanesov

