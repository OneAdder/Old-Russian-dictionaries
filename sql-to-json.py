import sqlite3
import json

db = sqlite3.connect('RusDict.db')
c = db.cursor()

'''
first json:
[
    {
        "lexeme_XI–XVII": "СТАРИЧЕКЪ",
        "lexeme_dict1": "лексема",
        "data_XI–XVII":
        {
            "Gram1": "м.",
            "Word2": "test",
            "Gram2": "test",
            "Link": "test",
            "Full": "%&Уменьш.-ласк. к старикъ (в знач. 1)&. Старичекъ, γερόντιον. Влх.Словарь, 156. XVII в."
        },
        "data_dict1":
        {
            ...
        }
    },
    {
        ...
    }.
    ...
]
'''

'''
second json:
{
    "СТАРИЧЕКЪ": {
        "data_XI–XVII":
        {
            "lexeme_XI–XVII": "СТАРИЧЕКЪ",
            "Gram1": "м.",
            "Word2": "test",
            "Gram2": "test",
            "Link": "test",
            "Full": "%&Уменьш.-ласк. к старикъ (в знач. 1)&. Старичекъ, γερόντιον. Влх.Словарь, 156. XVII в."
        },
        "data_dict1":
        {
            ...
        }
    },
    {
        ...
    }.
    ...
}
'''

data = c.execute('SELECT * FROM Words')

def get_first_json():
    js = []
    for line in data:
        line = ['' if el == "NULL" else el for el in line]
        document = {}
        document["lexeme_XI–XVII"] = line[1]
        document["data_XI–XVII"] = {"Gram1": line[2], "Word2": line[3], "Gram2": line[4], "Link": line[5], "Full": line[6]}
        js.append(document)
    with open("dat.json", "w", encoding='utf-8') as f:
        json.dump(js, f, indent=4, ensure_ascii=False)

def get_second_json():
    document = {}
    for line in data:
        line = ['' if el == "NULL" else el for el in line]
        document[line[1]] = {
            "data_XI–XVII": {
                "lexeme_XI–XVII": line[1],
                "Gram1": line[2],
                "Word2": line[3],
                "Gram2": line[4],
                "Link": line[5],
                "Full": line[6]
                }
            }
    with open("data.json", "w", encoding='utf-8') as f:
        json.dump(document, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    get_second_json()
