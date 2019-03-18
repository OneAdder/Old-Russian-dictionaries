"""В образовательных целях! Используйте unification.pyx!"""
import re

old_warning = True
if old_warning:
    print("Эта штука в репе как поучение, не надо её использовать! Используйте unification.pyx!")

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
    if not text:
        return ''
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

def unify_r_and_l_with_shwas1(text):
    """Превращаются сочетания:
    'согласный + р/л + ь/ъ + согласный' в 'согласный + є/о + р/л + согласный'
    'согласный + ь/ъ + р/л + согласный' в 'согласный + є/о + р/л + согласный'
    'согласный + р/л + ѣ + согласный' в 'согласный + р/л + є + согласный'
    """
    matches = re.findall('([' + set4 + '][рл][ьъ][' + set4 + '])', text)
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
    matches = re.findall('([' + set4 + '][ьъ][рл][' + set4 + '])', text)
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
    matches = re.findall('([' + set4 + '][рл]ѣ[' + set4 + '])', text)
    for match in matches:
        key = text.find(match)
        text = list(text)
        text[key + 2] = 'є'
        text = ''.join(text)
    return text



def drop_shwas(text):
    """Положить редуцированные."""
    text = list(text)
    i = len(text) - 1
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
    for i, sym in enumerate(text):
        if sym == text[-1]:
            if sym in set4:
                new_text += sym + 'ъ'
            else:
                new_text += sym
        else:
            if sym in set4 and text[i + 1] in set4:
                new_text += sym + 'ъ'
            else:
                new_text += sym
    return new_text
        
def replace_shwas(text):
    """Меняет редуцированные на є/о"""
    new_text = ''
    i = 0
    l = len(text)
    while i < l:
        if text[i] == 'ь':
            new_text += 'є'
        elif text[i] == 'ъ':
            new_text += 'о'
        else:
            new_text += text[i]
        i += 1

def pre_unify(text):
    """Унифицирует всё, кроме редуцированных."""
    if not text:
        return ''
    new_text = ''
    new_text = strip_stuff(text)
    new_text = unify_various_symbols(new_text)
    new_text = unify_final_shwa(new_text)
    new_text = unify_vowels_after_set1(new_text)
    new_text = unify_iotated(new_text)
    new_text = unify_i_and_front_shwa(new_text)
    new_text = unify_r_and_l_with_shwas1(new_text)
    new_text = unify_r_and_l_with_shwas2(new_text)
    new_text = unify_r_and_l_with_yat(new_text)
    return new_text

def unify(text):
    """Принимает слово на древнерусской языке и переводит его в унифицированный вид.
    
    Алгоритм сделан на основе статей:
    "Автоматический морфологический анализатор древнерусского языка: лингвистические и технологические решения". Баранов, Миронов, Лапин, Мельникова, Соколова, Корепанова.
    "ВЗIAЛЪ, ВЪЗЯЛЪ, ВЬЗЯЛ: ОБРАБОТКА ОРФОГРАФИЧЕСКОЙ ВАРИАТИВНОСТИ ПРИ ЛЕКСИКО-ГРАММАТИЧЕСКОЙ АННОТАЦИИ СТАРОРУССКОГО КОРПУСА XV–XVII ВВ.*". Т. С. Г АВРИЛОВА, Т. А. ШАЛГАНОВА, О. Н. ЛЯШЕВСКАЯ.

    Алгоритм унификации:
    1) Привести к нижнему регистру, удалить лишние знаки и т.д.
    2) Привести равнозначные знаки и фонологически незначимые отличия к единой форме. Подробнее см. unify_various_symbols
    3) Привести конечный редуцированный в "ъ".
    4) Уменьшить разнообразие гласные после после шипящих. Подробнее см. unify_vowels_after_set1
    5) Дезйотировать гласные в позиции начала слова и после гласных. Подробнее см. unify_iotated
    6) Перевести "ь" после йотированных гласных и "i" в "и".
    7) Преобразовать ряд сочетаний плавных с гласными. Подробнее см. unify_r_and_l_with_shwas1, unify_r_and_l_with_shwas2 и unify_r_and_l_with_yat
    8) Эмулировать падение редуцированных.
    9) Добавить принцип открытого слога.
    """
    if not text:
        return ''
    new_text = ''
    new_text = pre_unify(text)
    new_text = add_shwas(new_text)
    return new_text

def compare(word1, word2):
    """Данная функция сравнивает два слова тремя способами.
    
    1. Редуцированные упали/прояснились.
    2. Редуцированные добавились по принципу открытого слога.
    3. Редуцированные прояснились в є/о.
    4. Редуцированные добавились, после чего упали/прояснились.
    5. Редуцированные добавились, после чего прояснились в є/о.
    """
    pre_unified1 = pre_unify(word1)
    pre_unified2 = pre_unify(word2)
    
    word1_without_shwas = drop_shwas(pre_unified1)
    word2_without_shwas = drop_shwas(pre_unified2)
    if word1_without_shwas == word2_without_shwas:
        return add_shwas(word1_without_shwas)
    
    word1_with_open_shwa_vowels = add_shwas(pre_unified1)
    word2_with_open_shwa_vowels = add_shwas(pre_unified2)
    if word1_with_open_shwa_vowels == word2_with_open_shwa_vowels:
        return word1_with_open_shwa_vowels
    
    word1_replaced_shwas = replace_shwas(pre_unified1)
    word2_replaced_shwas = replace_shwas(pre_unified2)
    if word1_replaced_shwas == word2_replaced_shwas:
        return word1_replaced_shwas
    
    word1_with_dropped_open_shwa_vowels = drop_shwas(word1_with_open_shwa_vowels)
    word2_with_dropped_open_shwa_vowels = drop_shwas(word2_with_open_shwa_vowels)
    if word1_with_dropped_open_shwa_vowels == word2_with_dropped_open_shwa_vowels:
        return word1_with_dropped_open_shwa_vowels
    
    word1_added_replaced = replace_shwas(word1_with_open_shwa_vowels)
    word2_added_replaced = replace_shwas(word2_with_open_shwa_vowels)
    if word1_added_replaced == word2_added_replaced:
        return word1_added_replaced

    

def test1():
    words = ('врачение', 'ВРАЧЕНИ|Ѥ', 'напрѣждьспѣяние', 'ПОВѢЧ|Ь', 'пакы', 'ждѭ', 'дож', 'аѩдовитыйаꙓ',
             'прьивьiа', 'пьрцтълнлѣт', 'пьрцьси', 'всєдрьжитєлъ', 'ВЬСЕДЬРЖИТЕЛ|Ь', 'приь', 'прюьп', 'жю',
             'жюк', 'властелин', 'привет привет', 'пъпъпыпьпъпъпъпьпьпапъ', 'ка', 'к', 'трѢт', 'адвлѢвап')
    return map(unify, words)

def test2():
    word_pairs = (('врачение', 'ВРАЧЕНИ|Ѥ'), ('всєдрьжитєлъ', 'ВЬСЕДЬРЖИТЕЛ|Ь'), ('молъчание', 'мълчание'), ('молъчание', 'мълъчание'), ('молъчание', 'молчание'), ('мълчание', 'мълъчание'),
                  ('врачение', 'ВРАЧЕНИ|Ѥ'), ('всєдрьжитєлъ', 'ВЬСЕДЬРЖИТЕЛ|Ь'), ('молъчание', 'мълчание'), ('молъчание', 'мълъчание'), ('молъчание', 'молчание'), ('мълчание', 'мълъчание'))
    return (compare(*word_pair) for word_pair in word_pairs)
