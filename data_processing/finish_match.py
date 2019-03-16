"""Берёт те статьи из словаря XI-XVII, для которых не нашлось соответствий в словаре Аванесова. Пишет это всё в 'matched.json'."""
__author__ = "Michael Voronov, Anna Sorokina"
__license__ = "GPLv3"

import json
import pandas
import pyximport; pyximport.install()
from unification import unify

with open('prematched.json', 'r') as f:
    prematched = json.loads(f.read())

shit = pandas.read_csv('wordlist_linked.csv', delimiter=',', header=0)
x11 = list(shit.MainLemma)
x11 = [x11_lemma for x11_lemma in x11 if not unify(x11_lemma) in prematched]

for x11_lemma in x11:
    x11_unified = unify(x11_lemma)
    prematched[x11_unified] = {
        'XVII_lemma': x11_lemma
    }

with open('matched.json', 'w') as f:
    json.dump(prematched, f, indent=4, ensure_ascii=False) 
