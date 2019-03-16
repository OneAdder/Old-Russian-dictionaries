from bs4 import BeautifulSoup
import json
import pyximport; pyximport.install()
from unification import unify

with open('Словарь древнерусского языка (big).tei') as f:
    xml = f.read()
    
soup = BeautifulSoup(xml, 'xml')

#print(soup.superEntry.orth)


def get_avanesov_entries():
    entries = soup.find_all('superEntry')
    return entries

def convert_tei_to_json(entries):
    js = []
    for entry in entries:
        document = {}
        
        form = entry.form
        lemma = form.orth.text
        data = entry.sense
        
        if not form or not lemma or not data:
            continue
        
        examples_xml = data.find_all('cit')
        examples = []
        for example in examples_xml:
            ex_text = example.example_text
            if ex_text:
                subdoc = {
                    'example': ex_text.text,
                    'src': example.src.text
                }
                examples.append(subdoc)
            
        try:      
            if form['type'] == 'inflected':
                inflected = True
                inflection_xml = form.find_all('inflection')
                inflection = {}
                for inflec in inflection_xml:
                    inflection[inflec.lbl.text] = inflec.orth.text
            else:
                inflected = False
        except KeyError:
            inflected = False
            
        document['unified_lemma'] = unify(lemma)
        document['avanesov_lemma'] = lemma
        document['avanesov_data'] = {
            'gramGrp': form.gramGrp.pos.text,
            'definition': data.definition.text,
            'usg': form.usg.text,
            'inflected': inflected,
            'examples': examples
        }
        if inflected:
            document['avanesov_data']['inflection'] = inflection
        js.append(document)
    return js

def convert_tei_to_another_json(entries):
    js = {}
    for entry in entries:
        document = {}
        
        form = entry.form
        lemma = form.orth.text
        data = entry.sense
        
        if not form or not lemma or not data:
            continue
        
        examples_xml = data.find_all('cit')
        examples = []
        for example in examples_xml:
            ex_text = example.example_text
            if ex_text:
                subdoc = {
                    'example': ex_text.text,
                    'src': example.src.text
                }
                examples.append(subdoc)
            
        try:      
            if form['type'] == 'inflected':
                inflected = True
                inflection_xml = form.find_all('inflection')
                inflection = {}
                for inflec in inflection_xml:
                    inflection[inflec.lbl.text] = inflec.orth.text
            else:
                inflected = False
        except KeyError:
            inflected = False

        document['avanesov_lemma'] = lemma
        document['avanesov_data'] = {
            'gramGrp': form.gramGrp.pos.text,
            'definition': data.definition.text,
            'usg': form.usg.text,
            'inflected': inflected,
            'examples': examples
        }
        if inflected:
            document['avanesov_data']['inflection'] = inflection
        js[unify(lemma)] = document
    return js
        

def save(js):
    with open('avanesov2.json', 'w', encoding='utf-8') as f:
        json.dump(js, f, indent=4, ensure_ascii=False)

def main():
    entries = get_avanesov_entries()
    js = convert_tei_to_another_json(entries)
    save(js)

if __name__ == '__main__':
    main()
