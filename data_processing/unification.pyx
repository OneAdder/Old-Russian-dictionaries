#cython: language_level=3, boundscheck=False
"""Функции, которые приводят графику двух словарей в единый формат"""
__author__ = "Michael Voronov, Anna Sorokina"
__license__ = "GPLv3"

iotated = 'юиѭѩѥꙓꙑ'
set1 = {'ш', 'щ', 'ж', 'ч', 'ц'}
set2 = 'аоєѹiѧѫѣъьѵѷ' + iotated
set3 = 'i' + iotated
set4 = 'цкнгшщзхфвпрлджчсмтб'

def strip_stuff(text):
    """Приводит в нижний регистр и убирает '|' и прочее."""
    text = text.lower()
    new_text = ''
    cdef int i = 0
    cdef int l = len(text)
    while i < l:
        if text[i] == ('|'):
            i += 1
        elif text[i] == '.':
            i += 1
        elif text[i] == ' ':
            break
        else:
            new_text += text[i]
            i += 1
    return new_text

def unify_various_symbols(text):
    """Унифицирует разные варианты."""
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
    new_text = ''
    cdef int i = 0
    cdef int l = len(text)
    while i < l:
        if i + 1 == l:
            if text[i] in mapping:
                new_text += mapping[text[i]]
            else:
                new_text += text[i]
            i += 1
        else:
            if text[i] == 'о' and text[i+1] == 'у':
                new_text += 'ѹ'
                i += 2
            elif text[i] == 'ъ' and (text[i+1] == 'i' or text[i+1] == 'ї'):
                new_text += 'ꙑ'
                i += 2
            elif text[i] in mapping:
                new_text += mapping[text[i]]
                i += 1
            else:
                new_text += text[i]
                i += 1
    return new_text

def unify_final_shwa(text):
    """Приводит 'ъ' и 'ь' в конце к 'ъ'"""
    if text.endswith('ь'):
        text = text[:-1] + 'ъ'
    return text

def unify_vowels_after_set1(text):
    """Переводит нестрого йотированные после 'ш', 'щ', 'ж', 'жд', 'ч', 'ц' в строго не-йотированные.
    
    Мутная формулировка, но речь идёт о конкретных гласных и их фонологической релевантности после шипящих:
    ѧ/ѩ/а -> ѧ
    ѹ/ѫ/ѭ -> ѹ
    """
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
            elif text[i] == 'ж' and text[i+1] == 'д':
                if i + 2 == l:
                    new_text += text[i]
                    i += 1
                else:
                    if text[i + 2] in mapping:
                        new_text += text[i] + text[i+1] + mapping[text[i+2]]
                        i += 3
                    else:
                        new_text += text[i]
                        i += 1
            else:
                new_text += text[i]
                i += 1
    return new_text

def unify_iotated(text):
    """Убирает йотацию в начале слова и после гласных.
    
    Такая мера может показаться странной, так как в современном русском языке различение йотированных и нейотированных
    в позиции начала слова релевантно (ср. "ус" и "юс"). Однако, такое различение происходит прежде всего из противопоставления
    исконных слов и церковнославянских заимствований (ср. "аз" и "я"). В то время церковнославянский широко использовался
    носителями древнерусского, но чёткого различение не существовало.
    """
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
    """Превращает сочетание 'согласный + р/л + ь/ъ + согласный' в 'согласный + є/о + р/л + согласный'"""
    new_text = ''
    cdef int i = 0
    cdef int l = len(text)
    while i < l:
        if i + 3 >= l:
            new_text += text[i]
            i += 1
        else:
            if text[i] in set4 and text[i+1] in 'рл' and text[i+2] in 'ъь' and text[i+3] in set4:
                if text[i+2] == 'ь':
                    new_text += text[i] + 'є' + text[i+1] + text[i+3]
                else:
                    new_text += text[i] + 'о' + text[i+1] + text[i+3]
                i += 4
            else:
                new_text += text[i]
                i += 1
    return new_text



def unify_r_and_l_with_shwas2(text):
    """Превращает сочетание 'согласный + ь/ъ + р/л + согласный' в 'согласный + є/о + р/л + согласный'"""
    new_text = ''
    cdef int i = 0
    cdef int l = len(text)
    while i < l:
        if i + 3 >= l:
            new_text += text[i]
            i += 1
        else:
            if text[i] in set4 and text[i+1] in 'ъь' and text[i+2] in 'рл' and text[i+3] in set4:
                if text[i+1] == 'ь':
                    new_text += text[i] + 'є' + text[i+2] + text[i+3]
                else:
                    new_text += text[i] + 'о' + text[i+2] + text[i+3]
                i += 4
            else:
                new_text += text[i]
                i += 1
    return new_text

def unify_r_and_l_with_yat(text):
    """Превращает сочетание 'согласный + р/л + ѣ + согласный' в 'согласный + р/л + є + согласный'"""
    new_text = ''
    cdef int i = 0
    cdef int l = len(text)
    while i < l:
        if i + 3 >= l:
            new_text += text[i]
            i += 1
        else:
            if text[i] in set4 and text[i+1] in 'рл' and text[i+2] in 'ѣ' and text[i+3] in set4:
                new_text += text[i] + text[i+1] + 'є' + text[i+3]
                i += 4
            else:
                new_text += text[i]
                i += 1
    return new_text

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
    """Добавим редуцированные после ВСЕХ согласных не перед гласными."""
    new_text = ''
    cdef int i = 0
    cdef int l = len(text)
    while i < l:
        if i + 1 == l:
            if text[i] in set4:
                new_text += text[i] + 'ъ'
            else:
                new_text += text[i]
        else:
            if text[i] in set4 and not text[i + 1] in set2:
                new_text += text[i] + 'ъ'
            else:
                new_text += text[i]
        i += 1
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
             'прьивьiа', 'пьрцтълнлѣт', 'пьрцьси', 'всєдрьжитєлъ', 'ВЬСЕДЬРЖИТЕЛ|Ь', 'приь', 'прюьп', 'жю',
             'жюк', 'властелин', 'привет привет', 'пъпъпыпьпъпъпъпьпьпапъ', 'ка', 'к', 'трѢт', 'адвлѢвап')
    for word in words:
        print(unify(word))
