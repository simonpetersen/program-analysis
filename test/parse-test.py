import unittest
from microc.parser import ParserMicroC


class MCParser(unittest.TestCase):

    def test(self):
        file = open("microc.txt")
        program = file.read()
        mc_program = ParserMicroC(program).parse()
        file.close()
        self.assertEqual(len(mc_program.nodes), 7)
        pass


if __name__ == '__main__':
    unittest.main()