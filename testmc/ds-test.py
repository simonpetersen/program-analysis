import unittest
from analysis.analyzer import DetectingSignsAnalyser
from testmc.util import TestBase


class DetectionOfSignsTest(TestBase):
    def testAnalyzer(self):
        program = self.load("../test-files/base.txt")
        initialSigns = {'x': ['+','0','-'], 'y': ['+','0','-']}
        expected_variables = {'x','y'}
        analyzer = DetectingSignsAnalyser()
        nodeSigns = analyzer.analyze(program, initialSigns)
        expected_signs = []
        expected_signs.append([0, {'x': ['+', '0', '-'], 'y': ['+', '0', '-']}])
        expected_signs.append([1, {'x': ['+'], 'y': ['+', '0', '-']}])
        expected_signs.append([2, {'y': ['+'], 'x': ['+']}])
        expected_signs.append([3, {'x': ['+', '0', '-'], 'y': ['+']}])
        expected_signs.append([4, {'y': ['+'], 'x': ['+', '0', '-']}])
        expected_signs.append([5, {'x': ['+', '0', '-'], 'y': ['+']}])
        expected_signs.append([6, {'x': ['0'], 'y': ['+']}])

        #check variables
        self.assertEqual(program.variables(), expected_variables)
        nodes = program.nodeList()
        self.assertEqual(len(nodes), 6)
        # Check detection of signs
        self.assertEqual(nodeSigns[0], expected_signs[0])
        self.assertEqual(nodeSigns[1], expected_signs[1])
        self.assertEqual(nodeSigns[2], expected_signs[2])
        self.assertEqual(nodeSigns[3], expected_signs[3])
        self.assertEqual(nodeSigns[4], expected_signs[4])
        self.assertEqual(nodeSigns[5], expected_signs[5])
        self.assertEqual(nodeSigns[6], expected_signs[6])

if __name__ == '__main__':
    unittest.main()
