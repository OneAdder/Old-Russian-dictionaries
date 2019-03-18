echo 'Parsing TEI'
python3 tei_parser.py
echo 'Ready. The longest part is starting. Make some tea. This is gonna take some time (quadcore CPU: around 10m).'
python3 matcher.py
echo 'The longest part is over.'
python3 finish_match.py
echo 'Success!'
