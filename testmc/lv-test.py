import unittest
from analysis.analyser import LiveVariablesAnalyser
from analysis.worklist import WorklistChaotic
from testmc.util import TestBase


class TestReachingDefinitions(TestBase):

    def testLiveVariables(self):
        program = self.load("../test-files/base2.txt")
        analyzer = LiveVariablesAnalyser(program)
        nodes, constraints = analyzer.analyse()
        worklist = WorklistChaotic()
        input = worklist.computeSolution(constraints)
        output = []
        # Compute output for all nodes
        for i in range(0, len(input)):
            out = (input[i] - nodes[i].kill) | nodes[i].gen
            output.append(out)
        # Compare results to expected
        expected_input = [set(), {'y'}, {'x', 'y'}, {'y'}, {'z'}, {'z'}, set()]
        self.assertEqual(input, expected_input)
        expected_output = [set(), set(), {'y'}, {'x', 'y'}, {'y'}, {'y'}, {'z'}]
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
