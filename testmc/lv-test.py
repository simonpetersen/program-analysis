import unittest
from analysis.analyser import LiveVariablesAnalyser
from analysis.worklist import WorklistChaotic, WorklistFifo, WorklistLifo
from testmc.util import TestBase


class TestReachingDefinitions(TestBase):

    def testBase2Program(self):
        program = self.load("../test-files/base2.txt")
        analyzer = LiveVariablesAnalyser(program)
        nodes, constraints = analyzer.analyse()
        # Check kill/gen-sets
        self.assertEqual(nodes[0].kill, {'x'})
        self.assertEqual(nodes[0].gen, set())
        self.assertEqual(nodes[1].kill, {'y'})
        self.assertEqual(nodes[1].gen, set())
        self.assertEqual(nodes[2].kill, {'x'})
        self.assertEqual(nodes[2].gen, set())
        self.assertEqual(nodes[3].kill, set())
        self.assertEqual(nodes[3].gen, {'y', 'x'})
        self.assertEqual(nodes[4].kill, {'z'})
        self.assertEqual(nodes[4].gen, {'y'})
        self.assertEqual(nodes[5].kill, {'z'})
        self.assertEqual(nodes[5].gen, {'y'})
        self.assertEqual(nodes[6].kill, {'x'})
        self.assertEqual(nodes[6].gen, {'z'})

        expected_input = [set(), {'y'}, {'x', 'y'}, {'y'}, {'z'}, {'z'}, set()]
        input_chaotic = WorklistChaotic().computeSolution(constraints)
        # Compare results to expected
        self.assertEqual(expected_input, input_chaotic)

        input_fifo = WorklistFifo().computeSolution(constraints)
        # Compare results to expected
        self.assertEqual(expected_input, input_fifo)

        input_lifo = WorklistFifo().computeSolution(constraints)
        # Compare results to expected
        self.assertEqual(expected_input, input_lifo)

    def testMicrocProgram2(self):
        program = self.load("../test-files/microc2.txt")
        analyzer = LiveVariablesAnalyser(program)
        nodes, constraints = analyzer.analyse()
        # Check kill/gen-sets
        self.assertEqual(nodes[0].kill, {'z'})
        self.assertEqual(nodes[0].gen, set())
        self.assertEqual(nodes[1].kill, {'x'})
        self.assertEqual(nodes[1].gen, set())
        self.assertEqual(nodes[2].kill, set())
        self.assertEqual(nodes[2].gen, {'x'})
        self.assertEqual(nodes[3].kill, {'z'})
        self.assertEqual(nodes[3].gen, set())
        self.assertEqual(nodes[4].kill, set())
        self.assertEqual(nodes[4].gen, {'z'})
        self.assertEqual(nodes[5].kill, set())
        self.assertEqual(nodes[5].gen, {'x'})

        input_chaotic = WorklistChaotic().computeSolution(constraints)
        # Compare results to expected
        expected_input = [set(), {'y'}, {'x', 'y'}, {'y'}, {'z'}, {'z'}, set()]
        #self.assertEqual(expected_input, input_chaotic)


if __name__ == '__main__':
    unittest.main()
