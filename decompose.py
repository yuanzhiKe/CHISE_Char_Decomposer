import os
import argparse
import pickle
import traceback
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_file', help='Input file.', required=True)
parser.add_argument('-o', '--output_file', help='Output file.', required=True)
args = parser.parse_args()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def build_mapping():
    file_list = [
        'IDS-UCS-Basic.txt',
        'IDS-UCS-Compat-Supplement.txt',
        'IDS-UCS-Compat.txt',
        'IDS-UCS-Ext-A.txt',
        'IDS-UCS-Ext-B-1.txt',
        'IDS-UCS-Ext-B-2.txt',
        'IDS-UCS-Ext-B-3.txt',
        'IDS-UCS-Ext-B-4.txt',
        'IDS-UCS-Ext-B-5.txt',
        'IDS-UCS-Ext-B-6.txt',
        'IDS-UCS-Ext-C.txt',
        'IDS-UCS-Ext-D.txt',
        'IDS-UCS-Ext-E.txt',
        'IDS-UCS-Ext-F.txt'
    ]
    _map_dict = {}
    for fn in file_list:
        for _line in tqdm(open(fn), desc=u'Reading ' + fn):
            _line = _line.strip()
            if _line[0] != 'U':
                continue
            items = _line.split('\t')
            name = items[1]
            shape = items[2]
            _map_dict[name] = shape
    pickle.dump(_map_dict, open('chise_mapping.pkl', 'wb'))
    return _map_dict


def _is_chinese_char(cp):
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
        (cp >= 0x3400 and cp <= 0x4DBF) or  #
        (cp >= 0x20000 and cp <= 0x2A6DF) or  #
        (cp >= 0x2A700 and cp <= 0x2B73F) or  #
        (cp >= 0x2B740 and cp <= 0x2B81F) or  #
        (cp >= 0x2B820 and cp <= 0x2CEAF) or
        (cp >= 0xF900 and cp <= 0xFAFF) or  #
        (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
      return True
    return False


def decompose_chinese_character(char, map_dict):
    try:
        replace_seq = map_dict[char]
    except KeyError:
        replace_seq = char
    except Exception as e:
        traceback.print_exc()
        replace_seq = ''
        exit(-1)
    return replace_seq


def decompose(text, map_dict):
    out = ''
    for char in text:
        if _is_chinese_char(ord(char)):
            out += ' ' + decompose_chinese_character(char, map_dict) + ' '
        else:
            out += char
    return out


if __name__ == '__main__':
    if not os.path.isfile('chise_mapping.pkl'):
        map_dict = build_mapping()
    else:
        map_dict = pickle.load(open('chise_mapping.pkl', 'rb'))
    input_file = open(args.input_file, 'r')
    output_file = open(args.output_file, 'w')
    reader = tqdm(input_file, desc=u'Read 0 lines')
    i = 0
    for line in reader:
        output_line = decompose(line.strip('\r\n '), map_dict)
        output_line += '\n'
        output_file.write(output_line)
        i += 1
        if i % 100 == 0:
            reader.set_description(u'Read %s lines'%i)
    input_file.close()
    output_file.close()
