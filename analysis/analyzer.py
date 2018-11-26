from microc.statements import McAssignment
from microc.statements import McReadStatement
from analysis.data import UnionConstraint
from analysis.data import NodeInputSet
from analysis.data import NodeInputKillGen


class ReachingDefinitionsAnalyzer:

    def analyze(self, program):
        nodes = program.nodeList()
        variables = program.variables()
        flow = program.flow()
        assignments = self.assignments(nodes)

        self.setKillGenSets(nodes, assignments)
        return self.constructConstraints(nodes, variables, flow)

    # Returns the list of assignments in nodes of the program. Needed to define kill and gen sets.
    def assignments(self, nodes):
        assignments = set()
        for node in nodes:
            if type(node) is McAssignment:
                variables = node.lhs.variables()
                assignments = assignments | set(map(lambda v: (v, node.init), variables))
            elif type(node) is McReadStatement:
                variables = node.variables()
                assignments = assignments | set(map(lambda v: (v, node.init), variables))

        return assignments

    def setKillGenSets(self, nodes, assignments):
        for node in nodes:
            # Find kill and gen
            if type(node) is McAssignment:
                # Lhs of assignment will be variable, record or array. Handled by the variables-method,
                # which returns set of variables in expression.
                variables = node.lhs.variables()
                self.setNodeKillGen(node, variables, assignments)
            elif type(node) is McReadStatement:
                variables = node.variables()
                self.setNodeKillGen(node, variables, assignments)

    def setNodeKillGen(self, node, variables, assignments):
        kill = set(filter(lambda a: a[0] in variables, assignments)) | set(map(lambda v: (v, '?'), variables))
        gen = set(map(lambda v: (v, node.init), variables))
        node.kill, node.gen = kill, gen

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
