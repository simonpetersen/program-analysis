import unittest
from microc.parser import ParserMicroC


class TestBase(unittest.TestCase):

    def load(self, path):
        file = open(path)
        program = file.read()
        mc_program = ParserMicroC(program).parse()
        file.close()
        return mc_program