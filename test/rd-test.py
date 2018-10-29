import unittest
import microc.expressions
import microc.statements
import microc.microc
import microc.operations
from analysis.analyzer import ReachingDefinitionsAnalyzer
from analysis.worklist import ReachingDefinitionsWorklist


class TestReachingDefinitions(unittest.TestCase):

    def setUp(self):
        x = microc.expressions.McVariable(1, "x")
        y = microc.expressions.McVariable(2, "y")
        nodes = [microc.statements.McAssignment(1, x, microc.expressions.McValueLiteral(1, "5"))]
        nodes.append(microc.statements.McAssignment(2, y, microc.expressions.McValueLiteral(2, "1")))
        # Init content of while-statement
        condition = microc.operations.McGreaterThanOp(3, x, microc.expressions.McValueLiteral(3, "1"))
        y = microc.expressions.McVariable(4, "y")
        x = microc.expressions.McVariable(5, "x")
        y_assignment = microc.statements.McAssignment(4, y, microc.operations.McMultiplyOp(4, x, y))
        value = microc.expressions.McValueLiteral(5, "1")
        x_assignment = microc.statements.McAssignment(5, x, microc.operations.McMinusOp(5, x, value))
        # Append while-statement
        nodes.append(microc.statements.McWhileStatement(3, condition, [y_assignment, x_assignment]))
        # Append finale assignment to x
        x = microc.expressions.McVariable(6, "x")
        nodes.append(microc.statements.McAssignment(6, x, microc.expressions.McValueLiteral(6, "1")))

        self.program = microc.microc.McProgram(nodes)
        self.analyzer = ReachingDefinitionsAnalyzer()
        self.worklist = ReachingDefinitionsWorklist(self.program)

    def testAnalyzer(self):
        self.analyzer.analyze(self.program)
        expected_variables = {"x", "y"}
        self.assertEqual(self.program.variables(), expected_variables)
        nodes = self.program.nodeList()
        self.assertEqual(len(nodes), 6)
        # Check kill and gen sets
        self.assertEqual(nodes[0].gen, {('x', 1)})
        self.assertEqual(nodes[0].kill, {('x', '?'), ('x', 1), ('x', 5), ('x', 6)})
        self.assertEqual(nodes[1].gen, {('y', 2)})
        self.assertEqual(nodes[1].kill, {('y', '?'), ('y', 2), ('y', 4)})
        self.assertEqual(nodes[2].gen, set())
        self.assertEqual(nodes[2].kill, set())
        self.assertEqual(nodes[3].gen, {('y', 4)})
        self.assertEqual(nodes[3].kill, {('y', '?'), ('y', 2), ('y', 4)})
        self.assertEqual(nodes[4].gen, {('x', 5)})
        self.assertEqual(nodes[4].kill, {('x', '?'), ('x', 1), ('x', 5), ('x', 6)})
        self.assertEqual(nodes[5].gen, {('x', 6)})
        self.assertEqual(nodes[5].kill, {('x', '?'), ('x', 1), ('x', 5), ('x', 6)})

    def testWorklist(self):
        self.analyzer.analyze(self.program)
        rd_in, rd_out = self.worklist.computeSolution()
        # Check the output from the last node is correct.
        self.assertEqual(rd_out[6], {('x', 6), ('y', 4), ('y', 2)})


if __name__ == '__main__':
    unittest.main()
