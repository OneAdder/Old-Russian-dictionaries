#cython: language_level=3, boundscheck=False
"""Функции, которые приводят графику двух словарей в единый формат"""
__author__ = "Michael Voronov, Anna Sorokina"
__license__ = "GPLv3"

import re


iotated = 'юиѭѩѥꙓꙑ'
set1 = {'ш', 'щ', 'ж', 'ч', 'ц'}
set2 = 'аоєѹiѧѫѣъьѵѷ' + iotated
set3 = 'i' + iotated
set4 = 'цкнгшщзхфвпрлджчсмтб'

def strip_stuff(text):
    """Приводит в нижний регистр и убирает '|' и прочее."""
    text = text.lower()
    text = text.replace('|', '')
    text = re.sub(' .*', '', text)
    text = text.replace('.', '')
    return text

def unify_various_symbols(text):
    """Унифицирует разные варианты."""
    text = text.replace('оу', 'ѹ')
    text = re.sub('(ъi|ъї)', 'ꙑ', text)
    mapping = {
        'е': 'є',
        'э': 'є',
        'ѥ': 'є',
        'у': 'ѹ',
        'ꙋ': 'ѹ',
        'Ꙋ': 'ѹ',
        'ѡ': 'о',
        'ѿ': 'от',
        'ї': 'і',
        'ы': 'ꙑ',
        'ꙗ': 'ѧ',
        'я': 'ѧ',
        'ꙁ': 'з',
        'ѕ': 'з',
        'ѳ': 'ф',
        'ѯ': 'кс',
        'ѱ': 'пс',
        'ꙩ': 'о',
        'ꙫ': 'о',
        'ꙭ': 'о',
        'ꚙ': 'о',
        'ꚛ': 'о',
        'ꙮ': 'о',
        'ѽ': 'о',
        '҃': ''
    }
    text = ''.join([mapping[sym] if sym in mapping else sym for sym in text])
    return text

def unify_final_shwa(text):
    """Приводит 'ъ' и 'ь' в конце к 'ъ'"""
    if text.endswith('ь'):
        text = text[:-1] + 'ъ'
    return text

def unify_vowels_after_set1(text):
    """Переводит йотированные после 'ш', 'щ', 'ж', 'ч', 'ц' в не-йотированные."""
    mapping = {
        'а': 'ѧ',
        'ѩ': 'ѧ',
        'ю': 'ѹ',
        'ѫ': 'ѹ',
        'ѭ': 'ѹ'
    }
    new_text = ''
    cdef int l = len(text)
    cdef int i = 0
    while i < l:
        if i + 1 == l:
            new_text += text[i]
            i += 1
        else:
            if text[i] in set1 and text[i+1] in mapping:
                new_text += text[i] + mapping[text[i+1]]
                i += 2
            else:
                new_text += text[i]
                i += 1
    return new_text

def unify_iotated(text):
    """Убирает йотацию в начале слова и после гласных."""
    mapping = {
        'ю': 'ѹ',
        'ѩ': 'ѧ',
        'ѭ': 'ѫ',
        'ꙓ': 'ѣ'
    }
    new_text = ''
    cdef int i = 0
    cdef int l = len(text)
    while i < l:
        if i + 1 == l:
            new_text += text[i]
            i += 1
        else:
            if (text[i] in set2 and text[i+1] in mapping) or (i == 0 and text[i] in mapping):
                new_text += text[i] + mapping[text[i+1]]
                i += 2
            else:
                new_text += text[i]
                i += 1
    return new_text

def unify_i_and_front_shwa(text):
    """Превращает 'ь' после 'i' и йотированных в 'и'"""
    new_text = ''
    cdef int i = 0
    cdef int l = len(text)
    while i < l:
        if i + 1 == l:
            new_text += text[i]
            i += 1
        else:
            if text[i] in set3 and text[i+1] == 'ь':
                new_text += text[i] + 'и'
                i += 2
            else:
                new_text += text[i]
                i += 1
    return new_text

def unify_r_and_l_with_shwas1(text):
    """Превращается сочетание 'согласный + р/л + ь/ъ + согласный' в 'согласный + є/о + р/л + согласный'"""
    matches = re.findall('([' + set4 + '][рл][ьъ][' + set4 + '])', text)
    cdef int key
    for match in matches:
        key = text.find(match)
        v = text[key + 2]
        r = text[key + 1]
        text = list(text)
        if v == 'ь':
            text[key + 1] = 'є'
        else:
            text[key + 1] = 'о'
        text[key + 2] = r
        text = ''.join(text)
    return text

def unify_r_and_l_with_shwas2(text):
    """Превращается сочетание 'согласный + ь/ъ + р/л + согласный' в 'согласный + є/о + р/л + согласный'"""
    matches = re.findall('([' + set4 + '][ьъ][рл][' + set4 + '])', text)
    cdef int key
    for match in matches:
        key = text.find(match)
        r = text[key + 2]
        v = text[key + 1]
        text = list(text)
        if v == 'ь':
            text[key + 1] = 'є'
        else:
            text[key + 1] = 'о'
        text[key + 2] = r
        text = ''.join(text)
    return text

def unify_r_and_l_with_yat(text):
    """Превращается сочетание 'согласный + р/л + ѣ + согласный' в 'согласный + р/л + є + согласный'"""
    matches = re.findall('([' + set4 + '][рл]ѣ[' + set4 + '])', text)
    cdef int key
    for match in matches:
        key = text.find(match)
        text = list(text)
        text[key + 2] = 'є'
        text = ''.join(text)
    return text

def drop_shwas(text):
    """Положить редуцированные."""
    text = list(text)
    cdef int i = len(text) - 1
    drop_next = True
    while i >= 0:
        if text[i] in 'ъь':
            if drop_next:
                text.pop(i)
                drop_next = False
            else:
                if text[i] == 'ь':
                    text[i] = 'є'
                else:
                    text[i] = 'о'
                drop_next = True
        elif text[i] in set2:
            drop_next = True
        i -= 1
    return ''.join(text)


def add_shwas(text):
    """Добавим редуцированные."""
    new_text = ''
    cdef int i = 0
    cdef int l = len(text)
    while i < l:
        if text[i] == text[-1]:
            if text[i] in set4:
                new_text += text[i] + 'ъ'
            else:
                new_text += text[i]
        else:
            if text[i] in set4 and text[i + 1] in set4:
                new_text += text[i] + 'ъ'
            else:
                new_text += text[i]
        i += 1
    return new_text
        

#print(drop_shwas('пъпъпыпьпъпъпъпьпьпапъ'))

def unify(text):
    text = strip_stuff(text)
    text = unify_various_symbols(text)
    text = unify_final_shwa(text)
    text = unify_vowels_after_set1(text)
    text = unify_iotated(text)
    text = unify_i_and_front_shwa(text)
    text = unify_r_and_l_with_shwas1(text)
    text = unify_r_and_l_with_shwas2(text)
    text = unify_r_and_l_with_yat(text)
    text = drop_shwas(text)
    text = add_shwas(text)
    return text

def test():
    words = ('врачение', 'ВРАЧЕНИ|Ѥ', 'напрѣждьспѣяние', 'ПОВѢЧ|Ь', 'пакы', 'ждѭ', 'дож', 'аѩдовитыйаꙓ',
             'прьивьiа', 'пьрцтълнлѣт', 'пьрцьси', 'всєдрьжитєлъ', 'ВЬСЕДЬРЖИТЕЛ|Ь', 'приь', 'прюьп', 'жю', 'жюк', 'властелин')
    for word in words:
        print(unify(word))
