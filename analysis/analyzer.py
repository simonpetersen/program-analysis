from microc.statements import McAssignment
from analysis.data import UnionConstraint
from analysis.data import NodeInputSet
from analysis.data import NodeInputKillGen


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

        return nodes

    def constructConstraints(self, nodes, variables, flow):
        constraints = []
        for node in nodes:
            l = node.init
            if l == 1:
                base_set = set(map(lambda l: (l[0], '?'), variables))
                c = UnionConstraint(l, [NodeInputSet(l, base_set)])
                constraints.append(c)
            else:
                input = []
                conn_nodes = filter(lambda f: f[1] == l, flow)
                for n in conn_nodes:
                    i = n[0]
                    s = NodeInputKillGen(i, nodes[i-1].kill, nodes[i-1].gen)
                    input.append(s)
                c = UnionConstraint(l, input)
                constraints.append(c)

        return constraints

    def analyze(self, program):
        nodes = program.nodeList()
        variables = program.variables()
        flow = program.flow()
        assignments = self.assignments(nodes, set())

        nodes = self.setKillGenSets(nodes, assignments)
        return self.constructConstraints(nodes, variables, flow)
