"""Скрипт, который идёт по двум словарям и метчит их. Работает очень долго. Результат записывается в prematched.json.

Пояснение: Idle это не запускает, запускать можно просто интерпретатором python3.
Внешние зависимости: cython3.
Переменные:
    CPU_CORES: int (значение: 4)
        Если ядер больше четырёх, лучше разбить словарь на столько частей. сколько ядер.
    avanesov: dict
        JSON со словарём Аванесова.
    lengt: int
        Количество статей в словаре Аванесова, нужно для отображения прогресса.
    pool:
        Пул процессов.
    matched:
        Итоговый словарь.

Функции:
    splitDict(dict)
        Делит словарь на две части (взято с просторов сети Интернет.
    match_(dict)
        Функция на языке Cython из модуля match_cython. Принимает часть словаря Аванесова (или весь словарь),
        возвращает словарь, где для всех (по возможности) лемм были найдены соответствия из словаря XI-XVII.
"""

import json
import itertools

import pyximport; pyximport.install()
import match_cython

from multiprocessing import Pool
import os

CPU_CORES = 4

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

match_ = match_cython.match_

pool = Pool(processes=CPU_CORES)
matched1, matched2, matched3, matched4 = pool.map(match_, (avanesov1, avanesov2, avanesov3, avanesov4))
matched = {**matched1, **matched2, **matched3, **matched4}

with open('prematched.json', 'w') as f:
    json.dump(matched, f, indent=4, ensure_ascii=False)


