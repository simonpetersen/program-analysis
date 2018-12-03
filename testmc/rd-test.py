import unittest
from analysis.analyser import ReachingDefinitionsAnalyzer
from analysis.worklist import WorklistChaotic
from testmc.util import TestBase


class TestReachingDefinitions(TestBase):

    def testAnalyzer(self):
        program = self.load("../test-files/base.txt")
        analyzer = ReachingDefinitionsAnalyzer(program)
        nodes, constraints = analyzer.analyze()
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
        worklist = WorklistChaotic()
        solution = worklist.computeSolution(constraints)
        # Check the output from the last node is correct.
        self.assertEqual(solution[5], {('x', 5), ('y', 4), ('y', 2), ('x', 1)})


if __name__ == '__main__':
    unittest.main()
