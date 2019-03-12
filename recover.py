import os
import argparse
import pickle
import traceback
from tqdm import tqdm
from decompose import build_mapping

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_file', help='Input file.', required=True)
parser.add_argument('-o', '--output_file', help='Output file.', required=True)
args = parser.parse_args()

def _is_IDC(cp):
    if (cp >= 0x2FF0 and cp <= 0x2FFB):  #
      return True
    return False


def recover_chinese_character(radical_sequence, map_dict):
    try:
        char = map_dict[radical_sequence]
    except KeyError:
        char = radical_sequence
    except Exception as e:
        traceback.print_exc()
        char = ''
        exit(-1)
    return char


def recover(text, map_dict):
    out = ''
    for char in text.split(' '):
        if len(char) > 1 and _is_IDC(ord(char[0])):
            out += recover_chinese_character(char, map_dict)
        else:
            out += char
    return out

if __name__ == '__main__':
    if not os.path.isfile('chise_mapping.pkl'):
        map_dict = build_mapping()
    else:
        map_dict = pickle.load(open('chise_mapping.pkl', 'rb'))
    map_dict = {value: key for key, value in map_dict.items()}
    input_file = open(args.input_file, 'r')
    output_file = open(args.output_file, 'w')
    reader = tqdm(input_file, desc=u'Read 0 lines')
    i = 0
    for line in reader:
        output_line = recover(line.strip('\r\n '), map_dict)
        output_line += '\n'
        output_file.write(output_line)
        i += 1
        if i % 100 == 0:
            reader.set_description(u'Read %s lines'%i)
    input_file.close()
    output_file.close()
