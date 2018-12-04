import unittest
from testmc.util import TestBase
from microc.expressions import McVariableDeclaration
from microc.expressions import McRecordDeclaration
from microc.expressions import McArrayDeclaration
from microc.statements import McWhileStatement
from microc.statements import McAssignment
from microc.statements import McWriteStatement
from microc.statements import McIfStatement
from microc.statements import McIfElseStatement
from microc.statements import McReadStatement


class MCParserTest(TestBase):

    def testParseBase(self):
        program = self.load("../test-files/base.txt")
        self.assertEqual(len(program.nodes), 4)
        # Check type of nodes
        self.assertTrue(type(program.nodes[0]) is McAssignment)
        self.assertTrue(type(program.nodes[1]) is McAssignment)
        self.assertTrue(type(program.nodes[2]) is McWhileStatement)
        self.assertTrue(type(program.nodes[3]) is McAssignment)
        # Check body of while loop
        while_body = program.nodes[2].body
        self.assertTrue(type(while_body[0]) is McAssignment)
        # Check variables of lhs and rhs of assignment
        self.assertEqual(while_body[0].lhs.variables(), {'y'})
        self.assertEqual(while_body[0].rhs.variables(), {'y', 'x'})
        self.assertTrue(type(while_body[1]) is McAssignment)
        # Check variables of lhs and rhs of assignment
        self.assertEqual(while_body[1].lhs.variables(), {'x'})
        self.assertEqual(while_body[1].rhs.variables(), {'x'})

    def testParseBase2(self):
        program = self.load("../test-files/base2.txt")
        self.assertEqual(len(program.nodes), 5)
        self.assertTrue(type(program.nodes[0]) is McAssignment)
        self.assertTrue(type(program.nodes[1]) is McAssignment)
        self.assertTrue(type(program.nodes[2]) is McAssignment)
        self.assertTrue(type(program.nodes[3]) is McIfElseStatement)
        self.assertTrue(type(program.nodes[4]) is McAssignment)

    def testParseMicroC1(self):
        program = self.load("../test-files/microc1.txt")
        self.assertEqual(len(program.nodes), 7)
        # Check type of nodes
        self.assertTrue(type(program.nodes[0]) is McVariableDeclaration)
        self.assertTrue(type(program.nodes[1]) is McRecordDeclaration)
        self.assertTrue(type(program.nodes[2]) is McArrayDeclaration)
        self.assertTrue(type(program.nodes[3]) is McWhileStatement)
        self.assertTrue(type(program.nodes[4]) is McAssignment)
        self.assertTrue(type(program.nodes[5]) is McWhileStatement)
        self.assertTrue(type(program.nodes[6]) is McWriteStatement)

    def testParseMicroC2(self):
        program = self.load("../test-files/microc2.txt")
        self.assertEqual(len(program.nodes), 3)
        self.assertTrue(type(program.nodes[0]) is McVariableDeclaration)
        self.assertTrue(type(program.nodes[1]) is McAssignment)
        self.assertTrue(type(program.nodes[2]) is McIfStatement)
        # Check body of if-statement
        if_body = program.nodes[2].body
        self.assertEqual(len(if_body), 2)
        self.assertTrue(type(if_body[0]) is McReadStatement)
        self.assertTrue(type(if_body[1]) is McIfStatement)
        # Check nested if-body
        if_if_body = if_body[1].body
        self.assertEqual(len(if_if_body), 1)
        self.assertTrue(type(if_if_body[0]) is McWriteStatement)
        # Check variable in write statement.
        self.assertEqual(if_if_body[0].variables(), {'x'})


if __name__ == '__main__':
    unittest.main()