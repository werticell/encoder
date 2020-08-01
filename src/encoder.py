import argparse
import pickle
import math
from string import ascii_letters, ascii_lowercase
from src.open_file import Open


ALPHABET_POWER = len(ascii_lowercase)
ALPHABET_WITH_UPPER = set(ascii_letters)
ALPHABET = ascii_lowercase
DICT_FOR_TRANSFORMING = {key: value for value, key in enumerate(ascii_letters)}


def calculate_difference(frequencies, current_frequencies):
    result = 0.0
    for letter in ALPHABET:
        result += (frequencies.get(letter, 0) - current_frequencies.get(letter, 0)) ** 2
    return result


def rotate_dict_values(current_frequencies):
    keys = list(current_frequencies.values())
    keys = keys[1:] + keys[:1]
    for i, letter in enumerate(current_frequencies):
        current_frequencies[letter] = keys[i]


def break_caesar(input_file, output_file, frequencies):
    """
    Read txt-file, count frequencies of letters in it and tries to pick the right shift
    :param input_file: input directory
    :param output_file: output directory
    :param frequencies: dict of letter frequencies which user gave
    :return:
    """
    min_difference = math.inf
    most_probable_shift = 0
    current_frequencies = count_frequency(input_file)
    normalize_frequency(current_frequencies)
    for shift in range(ALPHABET_POWER):

        current_difference = calculate_difference(frequencies, current_frequencies)
        if current_difference < min_difference:
            most_probable_shift = shift
            min_difference = current_difference

        rotate_dict_values(current_frequencies)

    transform_txt(input_file, output_file, "caesar", most_probable_shift, "decode")


def count_freq_in_line(new_line, frequencies):
    new_line = new_line.lower()
    for letter in new_line:
        if letter in ALPHABET:
            frequencies[letter] += 1


def normalize_frequency(frequencies):
    letters_count = sum(frequencies.values())
    for letter in frequencies:
        frequencies[letter] /= letters_count


def count_frequency(input_file):
    """
    Read txt and count frequencies of letters in it
    :param input_file: input file
    :return:
    """
    frequencies = dict.fromkeys(ALPHABET, 0.0)
    with Open(input_file, "r") as fin:
        for new_line in fin:
            count_freq_in_line(new_line, frequencies)
    normalize_frequency(frequencies)
    return frequencies


def transform_symbol(letter, cipher_type, mode, key, key_shift=0):
    if letter not in ALPHABET_WITH_UPPER:
        return letter
    else:
        if cipher_type == "caesar" and mode == "decode":
            key %= ALPHABET_POWER
            return ascii_letters[(DICT_FOR_TRANSFORMING[letter] - key) % len(ascii_letters)]

        if cipher_type == "caesar" and mode == "encode":
            key %= ALPHABET_POWER
            return ascii_letters[(DICT_FOR_TRANSFORMING[letter] + key) % len(ascii_letters)]

        if cipher_type == "vigenere" and mode == "decode":
            return transform_symbol(letter, 'caesar', 'decode', DICT_FOR_TRANSFORMING[key[key_shift % len(key)]])

        if cipher_type == "vigenere" and mode == "encode":
            return transform_symbol(letter, 'caesar', 'encode',  DICT_FOR_TRANSFORMING[key[key_shift % len(key)]])


def transform_line(new_line, cipher_type, mode, key):
    if cipher_type == "caesar":
        result = [transform_symbol(letter, "caesar", mode, key) for letter in new_line]
        return ''.join(result)

    if cipher_type == "vigenere":
        result = [transform_symbol(letter, "vigenere", mode, key, shift) for shift, letter in enumerate(new_line)]
        return ''.join(result)


def transform_txt(input_file, output_file, cipher, key, mode):
    """
    Read txt-file and encode with a particular cipher
    :param input_file: input directory
    :param output_file: output directory
    :param cipher: cipher type that you code with
    :param key: key for encoding
    :param mode: says whether to decode or encode file
    """
    with Open(output_file, "w") as fout, Open(input_file, "r") as fin:
        for new_line in fin:
            fout.write(transform_line(new_line, cipher, mode, key))


def create_parser():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode')
    code_parser = subparsers.add_parser('encode')
    code_parser.add_argument('--input_file')
    code_parser.add_argument('--output_file')
    code_parser.add_argument('--cipher', choices=['caesar', 'vigenere'], required=True)
    code_parser.add_argument('--key', required=True)

    code_parser = subparsers.add_parser('decode')
    code_parser.add_argument('--input_file')
    code_parser.add_argument('--output_file')
    code_parser.add_argument('--cipher', choices=['caesar', 'vigenere'], required=True)
    code_parser.add_argument('--key', help='A key to encode/decode your file (int/string for caesar/vigenere)',
                             required=True)

    count_parser = subparsers.add_parser('count_freq')
    count_parser.add_argument('--input_file', required=True)
    count_parser.add_argument('--freq_file', default="stats.txt", required=True)

    break_parser = subparsers.add_parser('break')
    break_parser.add_argument('--input_file', required=True)
    break_parser.add_argument('--output_file', required=True)
    break_parser.add_argument('--freq_file', default="stats.txt", required=True)
    return parser


def main():

    parser = create_parser()
    args = parser.parse_args()

    if args.mode == "encode" or args.mode == "decode":
        cipher = args.cipher.lower()
        key = int(args.key) if cipher == "caesar" else args.key

        transform_txt(args.input_file, args.output_file, args.cipher.lower(), key, args.mode)

    if args.mode == "count_freq":
        frequencies = count_frequency(args.input_file)

        with open(args.freq_file, "wb") as fout:
            pickle.dump(frequencies, fout)

    if args.mode == "break":
        with open(args.freq_file, "rb") as fin:
            frequencies = pickle.load(fin)

        break_caesar(args.input_file, args.output_file, frequencies)


if __name__ == '__main__':
    main()
