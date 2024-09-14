#For running write " python language_detection.py test_ready.csv test_res.csv " in GitBash

# coding: utf-8

# In[1]:

import sys
import argparse
import csv

from langdetect import detect


# In[17]:

def readargs():
    parser = argparse.ArgumentParser(description='Detect language in which texts are written.')

    # TODO: remove hack
#     parser.add_argument('-f', nargs='?')

    # Specify CSV delimiter
    parser.add_argument('-d', dest='delimiter', default=';')

    # A flag that tells to produce output without text
    parser.add_argument('--short', dest='skiptext', action='store_true', default=False)

    # Specify an input file or read directly from stdin.
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r', encoding='UTF-8', errors='ignore'), default=sys.stdin)

    # Specify an output file or write directly to stdout.
    parser.add_argument('output_file', nargs='?', type=argparse.FileType('w', encoding='UTF-8', errors='ignore'), default=sys.stdout)

    return parser.parse_args()


# In[22]:

def get_lang(text):
    try:
        return detect(text)
    except Exception as e:
        sys.stderr.write('Warning: ' + str(e) + '\n')
        return

def skiptext(row, flag=False):
    if (flag):
        row.pop('text') if isinstance(row, dict) else row.remove('text')
    return row


# In[15]:

def main():
    # read arguments
    args = readargs()

    input_rows = csv.DictReader(
        args.input_file,
        fieldnames=['supplier_hotel_id','supplier_id', 'supplier_name', 'type', 'culture', 'len', 'text'],
        delimiter=args.delimiter
    )
    output_rows = csv.DictWriter(
        args.output_file,
        fieldnames=skiptext(['supplier_hotel_id', 'supplier_id', 'supplier_name', 'type', 'culture', 'culture_detected', 'len', 'text'], args.skiptext),
        delimiter=args.delimiter,
        lineterminator='\n'
    )

    # skip the header
    next(input_rows)
    output_rows.writeheader()

    #
    for row in input_rows:
        r = {
            'supplier_hotel_id': row['supplier_hotel_id'],
            'supplier_id': row['supplier_id'],
            'supplier_name': row['supplier_name'],
            'type' : row['type'],
            'culture': row['culture'],
            'culture_detected': get_lang(row['text']),
            'len': row['len'],
            'text': row['text']
        }
        output_rows.writerow(skiptext(r, args.skiptext))


# In[23]:

main()

