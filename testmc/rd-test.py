import unittest
from analysis.analyser import ReachingDefinitionsAnalyzer
from analysis.worklist import WorklistChaotic, WorklistFifo, WorklistLifo
from testmc.util import TestBase


class TestReachingDefinitions(TestBase):

    def testBaseProgram(self):
        program = self.load("../test-files/base.txt")
        analyzer = ReachingDefinitionsAnalyzer(program)
        nodes, constraints = analyzer.analyse()
        expected_variables = {"x", "y"}
        self.assertEqual(program.variables(), expected_variables)
        nodes = program.nodeList()
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

        # Test worklist implementation
        expected_solution = [{('x', '?'), ('y', '?')}, {('x', 1), ('y', '?')}, {('x', 1), ('y', 2), ('x', 5), ('y', 4)},
                             {('x', 1), ('y', 2), ('x', 5), ('y', 4)}, {('x', 1), ('y', 4), ('x', 5)},
                             {('x', 5), ('y', 4), ('y', 2), ('x', 1)}]
        solution_chaotic = WorklistChaotic().computeSolution(constraints)
        # Check the output from the last node is correct.
        self.assertEqual(solution_chaotic, expected_solution)

        solution_fifo = WorklistFifo().computeSolution(constraints)
        # Check the output from the last node is correct.
        self.assertEqual(solution_fifo, expected_solution)

        solution_lifo = WorklistLifo().computeSolution(constraints)
        # Check the output from the last node is correct.
        self.assertEqual(solution_fifo, expected_solution)

    def testMcProgram2(self):
        program = self.load("../test-files/microc2.txt")
        analyzer = ReachingDefinitionsAnalyzer(program)
        nodes, constraints = analyzer.analyse()
        expected_variables = {"x", "z"}
        self.assertEqual(program.variables(), expected_variables)
        nodes = program.nodeList()
        self.assertEqual(len(nodes), 6)
        # Check kill and gen sets
        self.assertEqual(nodes[0].gen, {('z', 1)})
        self.assertEqual(nodes[0].kill, {('z', '?'), ('z', 1), ('z', 4)})
        self.assertEqual(nodes[1].gen, {('x', 2)})
        self.assertEqual(nodes[1].kill, {('x', '?'), ('x', 2)})
        self.assertEqual(nodes[2].gen, set())
        self.assertEqual(nodes[2].kill, set())
        self.assertEqual(nodes[3].gen, {('z', 4)})
        self.assertEqual(nodes[3].kill, {('z', '?'), ('z', 1), ('z', 4)})
        self.assertEqual(nodes[4].gen, set())
        self.assertEqual(nodes[4].kill, set())
        self.assertEqual(nodes[5].gen, set())
        self.assertEqual(nodes[5].kill, set())

        # Test worklist implementation
        expected_solution = set()
        solution_chaotic = WorklistChaotic().computeSolution(constraints)
        # Check the input for the last node is correct.
        self.assertEqual(solution_chaotic[5], expected_solution)

        solution_fifo = WorklistFifo().computeSolution(constraints)
        self.assertEqual(solution_fifo[5], expected_solution)

        solution_lifo = WorklistLifo().computeSolution(constraints)
        self.assertEqual(solution_fifo[5], expected_solution)


if __name__ == '__main__':
    unittest.main()
