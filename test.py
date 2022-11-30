import unittest

from tokenizer_c_ansi import tokenize

class TestTokenize(unittest.TestCase):
    def test_regex(self):
        for name, tokenNum in [['teste-arithmetic-operators.c', 137], ['teste-double.c', 63], ['teste-float.c', 45]]:
            f = open(name, 'r', encoding='utf-8')
            text = "".join(stripped for stripped in f.readlines())
            tokens = list(tokenize(text))

            self.assertEqual(len(tokens), tokenNum)
            f.close()



    def test_identifier(self):
        self.assertEqual(1,1)

    def test_number(self):
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()