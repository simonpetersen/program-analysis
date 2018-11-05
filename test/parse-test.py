import unittest
from microc.parser import ParserMicroC


class MCParser(unittest.TestCase):

    def test(self):
        file = open("microc.txt")
        program = file.read()
        ParserMicroC(program).parse()
        file.close()


if __name__ == '__main__':
    unittest.main()