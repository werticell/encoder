import pytest
import pickle

from src.encoder import transform_txt, count_frequency, break_caesar


class TestEncodeDecode:

    @pytest.mark.parametrize("text_file, key", [
        ('src_tests/Alice.txt', 16),
        ('src_tests/Earth.txt', 37),
        ('src_tests/Ladder.txt', 31),
        ('src_tests/Plato.txt', 28)
    ])
    def test_caesar_encode_decode(self, text_file, key):
        encoded_file = 'src_tests/encoded.txt'
        decoded_file = 'src_tests/decoded.txt'
        transform_txt(text_file, encoded_file, 'caesar', key, 'encode')
        transform_txt(encoded_file, decoded_file, 'caesar', key, 'decode')
        assert open(text_file).read() == open(decoded_file).read()

    @pytest.mark.parametrize("text_file, key_word", [
        ('src_tests/Alice.txt', 'python'),
        ('src_tests/Earth.txt', 'lemon'),
        ('src_tests/Ladder.txt', 'attackathigth'),
        ('src_tests/Plato.txt', 'mipttpim')
    ])
    def test_vigenere_encode_decode(self, text_file, key_word):
        encoded_file = 'src_tests/encoded.txt'
        decoded_file = 'src_tests/decoded.txt'
        transform_txt(text_file, encoded_file, 'vigenere', key_word, 'encode')
        transform_txt(encoded_file, decoded_file, 'vigenere', key_word, 'decode')
        assert open(text_file).read() == open(decoded_file).read()


class TestCountBreak:

    @pytest.mark.parametrize("train_file, text_file, key", [
        ('src_tests/Earth.txt', 'src_tests/Alice.txt', 16),
        ('src_tests/Ladder.txt', 'src_tests/Earth.txt', 37),
        ('src_tests/Plato.txt', 'src_tests/Ladder.txt', 31),
        ('src_tests/Alice.txt', 'src_tests/Plato.txt', 28)
    ])
    def test_caesar_break(self, train_file, text_file, key):
        encoded_file = 'src_tests/encoded.txt'
        decoded_file = 'src_tests/decoded.txt'
        frequencies = count_frequency(train_file)

        transform_txt(text_file, encoded_file, 'caesar', key, 'encode')
        break_caesar(encoded_file, decoded_file, frequencies)
        assert open(text_file).read() == open(decoded_file).read()


if __name__ == '__main__':
    pytest.main()
