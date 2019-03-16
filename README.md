# Установка
Установка с помощью пакетных менеджеров не предусмотрена. Следует просто клонировать репозиторий.

`git clone https://github.com/OneAdder/Old-Russian-dictionaries`

# Запуск
Для запуска веб-приложения следует третьим Питоном запустить `old_rus_dictionaries.py`

Зависимости: `Flask`.



Для запуска обработки словарей следут запустить Башем скрипт `./data_processing/match.sh` (пользователи Windows могут запустить скрипты по порядку: `./data_processing/tei_parser.py`, `./data_processing/matcher.py` и `./data_processing/finish_match.py`). Результаты выведутся в файл `./data_processing/matched.json`.

Зависимости: `cython3`, `pandas`, `bs4`.
