"""Функции, которые приводят графику двух словарей в единый формат"""
import re

iotated = 'юиѭѩѥꙓꙑ'
set1 = {'ш', 'щ', 'ж', 'ч', 'ц'}
set2 = 'аоєѹiѧѫѣъьѵѷ' + iotated
set3 = 'i' + iotated
set4 = 'цкнгшщзхфвпрлджчсмтб'

def strip_stuff(text):
    """Приводит в нижний регистр и убирает '|'."""
    text = text.lower()
    text = text.replace('|', '')
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
    """Переводит йотированные после 'ш', 'щ', 'ж', 'ч', 'ц' в не-йотированные. В идеале стоит переписать получше."""
    mapping = {
        'а': 'ѧ',
        'ѩ': 'ѧ',
        'ю': 'ѹ',
        'ѫ': 'ѹ',
        'ѭ': 'ѹ'
    }
    new_text = ''
    i = 0
    while i < len(text):
        if text[i] in set1:
            try:
                if text[i + 1] == 'д':
                    if text [i + 2] in mapping:
                        new_text += text[i] + text[i + 1] + mapping[text[i + 2]]
                        i += 3
                    else:
                        new_text += text[i]
                        i += 1
                elif text[i + 1] in mapping:
                    new_text += text[i] + mapping[text[i + 1]]
                    i += 2
                else:
                    new_text += text[i]
                    i += 1
            except IndexError:
                new_text += text[i]
                i += 1
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
    if text[0] in mapping:
        text[0] = mapping[text[0]]
    matches = re.findall('([' + set2 + '][' + ''.join(mapping.keys()) + '])', text)
    for match in matches:
        key = text.find(match) + 1
        text = list(text)
        text[key] = mapping[text[key]]
        text = ''.join(text)
    return text

def unify_i_and_front_shwa(text):
    """Превращает 'ь' после 'i' и йотированных в 'и'"""
    matches = re.findall('([ь][' + set3 + '])', text)
    for match in matches:
        key = text.find(match)
        text = list(text)
        text[key] = 'и'
        text = ''.join(text)
    return text

def unify_r_and_l_with_vowels(text):
    """Превращаются сочетания:
    'согласный + ь/ъ + р/л + согласный' в 'согласный + р/л + ь/ъ + согласный'
    'согласный + р/л + ѣ + согласный' в 'согласный + р/л + є + согласный'
    """
    matches = re.findall('((?:[' + set4 + '])(?:[ьъ])(?:[рл])(?:[' + set4 + ']))', text)
    for match in matches:
        key = text.find(match)
        v = text[key + 2]
        r = text[key + 1]
        text = list(text)
        text[key + 1] = v
        text[key + 2] = r
        text = ''.join(text)
    matches = re.findall('([' + set4 + '][рл]ѣ[' + set4 + '])', text)
    for match in matches:
        key = text.find(match)
        text = list(text)
        text[key + 2] = 'є'
        text = ''.join(text)
    return text

def drop_shwas(text):
    matches = re.findall('([' + set4 + '][ь][' + set4 + '])', text)
    for match in matches:
        key = text.find(match)
        text = list(text)
        text[key + 1] = 'є'
        text = ''.join(text)
    matches = re.findall('([' + set4 + '][ъ][' + set4 + '](?:^[иѧ]\b))', text)
    for match in matches:
        key = text.find(match)
        text = list(text)
        text[key + 1] = 'о'
        text = ''.join(text)
    return text

def unify(text):
    text = strip_stuff(text)
    text = unify_various_symbols(text)
    text = unify_final_shwa(text)
    text = unify_vowels_after_set1(text)
    text = unify_iotated(text)
    text = unify_i_and_front_shwa(text)
    text = unify_r_and_l_with_vowels(text)
    text = drop_shwas(text)
    return text

def test():
    words = ('врачение', 'ВРАЧЕНИ|Ѥ', 'напрѣждьспѣяние', 'ПОВѢЧ|Ь', 'пакы', 'ждѭ', 'дож', 'аѩдовитыйаꙓ', 'прьивьiа', 'пьрцтълнлѣт', 'пьрцьси')
    for word in words:
        print(unify(word))
#test()
