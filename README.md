# Установка
Установка с помощью пакетных менеджеров не предусмотрена. Следует просто клонировать репозиторий.

`git clone https://github.com/OneAdder/Old-Russian-dictionaries`

# Запуск
Для запуска веб-приложения следует третьим Питоном запустить `old_rus_dictionaries.py`

Зависимости: `Flask`, `cython3`.



Для запуска обработки словарей следут запустить Башем скрипт `data_processing/match.sh` (пользователи Windows могут запустить Питоном скрипты по порядку: `data_processing/tei_parser.py`, `data_processing/matcher.py` и `data_processing/finish_match.py`). Результаты выведутся в файл `data_processing/matched.json`.

Зависимости: `cython3`, `pandas`, `bs4`.

# Устройство данных
Устройство JSON-файла `data_processing/matched.json`


```
{
    унифицированная_лемма (str):
     {
        "avanesov_lemma": XI-XIV_лемма (str),
        "avanesov_data": {
        "gramGrp": граматический_клас (str),
        "definition": определение (str),
        "usg": использование (str),
        "inflected": изменяемый/неизменяемый (bool),
        "examples": 
        [
            {
                example": пример (str),
                "src": источник (str)
            },
            ...
        ],
        "inflection": {формы (dict)}
        }
        "XVII_lemma": XI-XVII_лемма
    },
   ...
}
```

# Библиотека unification
Мы создали библиотеку `data_processing/unification.pyx`. Эта библиотека на языке Cython содержит функцию `unify`, которая принимает слово (`str`) и приводит его к единому формату. Таким образом, можно сравнить два слова: если они одинаковые (например, "вседержитель" и "вьседержитель"), то `unify` выдаст один результат для обоих слов.

Алгоритм сделан на основе статей:
* "Автоматический морфологический анализатор древнерусского языка: лингвистические и технологические решения"
Баранов, Миронов, Лапин, Мельникова, Соколова, Корепанова.

* "ВЗIAЛЪ, ВЪЗЯЛЪ, ВЬЗЯЛ: ОБРАБОТКА ОРФОГРАФИЧЕСКОЙ ВАРИАТИВНОСТИ ПРИ ЛЕКСИКО-ГРАММАТИЧЕСКОЙ АННОТАЦИИ СТАРОРУССКОГО КОРПУСА XV–XVII ВВ." Т. С. Г АВРИЛОВА, Т. А. ШАЛГАНОВА, О. Н. ЛЯШЕВСКАЯ.

Алгоритм унификации:
1. Привести к нижнему регистру, удалить лишние знаки и т.д.
2. Привести равнозначные знаки и фонологически незначимые отличия к единой форме. Подробнее см. докстринги `unify_various_symbols`.
3. Привести конечный редуцированный в "ъ".
4. Уменьшить разнообразие гласные после после шипящих. Подробнее см. докстринги `unify_vowels_after_set1`.
5. Дезйотировать гласные в позиции начала слова и после гласных. Подробнее см. докстринги unify_iotated
6. Перевести "ь" после йотированных гласных и "i" в "и".
7. Преобразовать ряд сочетаний плавных с гласными. Подробнее см. докстринги `unify_r_and_l_with_shwas1`, `unify_r_and_l_with_shwas2` и `unify_r_and_l_with_yat`.
8. Эмулировать падение редуцированных.
9. Добавить принцип открытого слога.

# Скрипт для обработки данных
Скрипт match.sh обрабатывает все имеющиеся данные и приводит в matched.json. Данный Bash-скрипт запускает скрипты на языке Python3. Порядок следующий:
1. `tei_parser.py`: парсит словарь Аванесова в формате `TEI` и сохраняет в `avanesov2.json`.
2. `matcher.py`: проходится по словарю Аванесова и ищет аналоги из словаря XI-XVII. Импортирует модули `match_cython` и `unification`, написанные на Cython. Сохраняет результат в `prematched.json`.
3. `finish_match.py`: вставляет данные из словаря XI-XVII, для которых не нашлось соответствий в словаре Аванесова, и сохраняет результат в `matched.json`.

# Использование
Данный код свободно распространяется под лицензией GNU GPLv3. Это значит, что вы можете свободно его использовать при условии, что оставите его открытым и упомяните его авторов.
Если вы собираетесь использовать его в начных публикациях, нам будет приятно, если вы упомяните нас так же в благодарностях.
