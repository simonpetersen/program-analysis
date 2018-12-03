import unittest
from microc.parser import ParserMicroC
from microc.expressions import McVariableDeclaration
from microc.expressions import McRecordDeclaration
from microc.expressions import McArrayDeclaration
from microc.statements import McWhileStatement
from microc.statements import McAssignment
from microc.statements import McWriteStatement
from microc.statements import McIfStatement


class MCParserTest(unittest.TestCase):

    def testParseBase(self):
        program = self.load("../testmc-files/base.txt")
        self.assertEqual(len(program.nodes), 4)
        self.assertTrue(type(program.nodes[0]) is McAssignment)
        self.assertTrue(type(program.nodes[1]) is McAssignment)
        self.assertTrue(type(program.nodes[2]) is McWhileStatement)
        self.assertTrue(type(program.nodes[3]) is McAssignment)

    def testParseMicroC1(self):
        program = self.load("../testmc-files/microc1.txt")
        self.assertEqual(len(program.nodes), 7)
        self.assertTrue(type(program.nodes[0]) is McVariableDeclaration)
        self.assertTrue(type(program.nodes[1]) is McRecordDeclaration)
        self.assertTrue(type(program.nodes[2]) is McArrayDeclaration)
        self.assertTrue(type(program.nodes[3]) is McWhileStatement)
        self.assertTrue(type(program.nodes[4]) is McAssignment)
        self.assertTrue(type(program.nodes[5]) is McWhileStatement)
        self.assertTrue(type(program.nodes[6]) is McWriteStatement)

    def testParseMicroC2(self):
        program = self.load("../testmc-files/microc2.txt")
        self.assertEqual(len(program.nodes), 3)
        self.assertTrue(type(program.nodes[2]) is McIfStatement)


if __name__ == '__main__':
    unittest.main()