from microc.statements import McAssignment


class ReachingDefinitionsAnalyzer:
    def assignments(self, nodes, assignments):
        for node in nodes:
            if type(node) is McAssignment:
                assignments = assignments | {(node.lhs.variable, node.init)}

        return assignments

    def setKillGenSets(self, nodes, assignments):
        for node in nodes:
            # Find kill and gen
            if type(node) is McAssignment:
                variable = node.lhs.variable
                kill = set(filter(lambda a: variable == a[0], assignments)) | {(variable, '?')}
                gen = {(variable, node.init)}
                node.kill, node.gen = kill, gen

    def analyze(self, program):
        nodes = program.nodeList()
        assignments = self.assignments(nodes, set())

        self.setKillGenSets(nodes, assignments)
