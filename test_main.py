import pytest

from src.encoder import transform_txt, count_frequency, break_caesar, transform_line


class TestEncodeDecode:

    @pytest.mark.parametrize("input_string, output_string, key", [
        ('aBcか', 'cDeか', 2),
        ('mipt_python_review', 'vryC_yHCqxw_AnErnF', 9),
        ('LeMon', 'QjRts', 5),
        ('encodIng_teXt', 'oxmynSxq_DohD', 10),
        ('attackatdawn', 'iBBiksiBliEv', 8),
    ])
    def test_caesar_transform_line(self, input_string, output_string, key):
        assert transform_line(input_string, 'caesar', 'encode', key) == output_string

    @pytest.mark.parametrize("text_file, key", [
        ('src_tests/Alice.txt', 16),
        ('src_tests/Earth.txt', 37),
        ('src_tests/Ladder.txt', 31),
        ('src_tests/Plato.txt', 28),
        ('src_tests/Earth.txt', -17),
    ])
    def test_caesar_encode_decode(self, text_file, key):
        encoded_file = 'src_tests/encoded.txt'
        decoded_file = 'src_tests/decoded.txt'
        transform_txt(text_file, encoded_file, 'caesar', key, 'encode')
        transform_txt(encoded_file, decoded_file, 'caesar', key, 'decode')
        with open(text_file, 'r') as text_file, open(decoded_file, 'r') as decoded_file:
            assert text_file.read() == decoded_file.read()

    @pytest.mark.parametrize("input_string, output_string, key", [
        ('aBcか', 'bCdか', 'B'),
        ('mipt_python_review', 'xmFE_FJxxzr_CiLtiM', 'leq'),
        ('LeMon', 'QhRrs', 'fd'),
        ('encodIng_teXt', 'eyczdTnr_Eeit', 'al'),
        ('attackatdawn', 'lxFopveFrnHr', 'lemon'),
    ])
    def test_vigenere_transform_line(self, input_string, output_string, key):
        assert transform_line(input_string, 'vigenere', 'encode', key) == output_string

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
        with open(text_file, 'r') as text_file, open(decoded_file, 'r') as decoded_file:
            assert text_file.read() == decoded_file.read()


class TestCountBreak:

    @pytest.mark.parametrize("train_file, text_file, key", [
        ('src_tests/Earth.txt', 'src_tests/Alice.txt', 16),
        ('src_tests/Ladder.txt', 'src_tests/Earth.txt', 37),
        ('src_tests/Plato.txt', 'src_tests/Ladder.txt', 31),
        ('src_tests/Alice.txt', 'src_tests/Plato.txt', 28),
        ('src_tests/Earth.txt', 'src_tests/Alice.txt', -17),
    ])
    def test_caesar_break(self, train_file, text_file, key):
        encoded_file = 'src_tests/encoded.txt'
        decoded_file = 'src_tests/decoded.txt'
        frequencies = count_frequency(train_file)

        transform_txt(text_file, encoded_file, 'caesar', key, 'encode')
        break_caesar(encoded_file, decoded_file, frequencies)
        with open(text_file, 'r') as text_file, open(decoded_file, 'r') as decoded_file:
            assert text_file.read() == decoded_file.read()


if __name__ == '__main__':
    pytest.main()
