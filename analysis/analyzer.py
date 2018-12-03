from microc.statements import McAssignment
from microc.statements import McReadStatement
from microc.statements import McWhileStatement
from microc.statements import McIfStatement
from microc.statements import McIfElseStatement
from analysis.data import UnionConstraint
from analysis.data import NodeInputSet
from analysis.data import NodeInputKillGen
from abc import ABC, abstractmethod


class BitVectorAnalyzerBase(ABC):
    def __init__(self, program):
        self.nodes = program.nodeList()
        self.flow = program.flow()
        self.base_case = [1]
        self.base_set = set()

    def analyze(self):
        self.setKillGenSets(self.nodes)
        return self.nodes, self.constructConstraints(self.nodes)

    @abstractmethod
    def setKillGenSets(self, nodes):
        pass

    def constructConstraints(self, nodes):
        constraints = []
        for node in nodes:
            l = node.init
            if l in self.base_case:
                c = UnionConstraint(l, [NodeInputSet(l, self.base_set)])
                constraints.append(c)
            else:
                input = []
                conn_nodes = filter(lambda f: f[1] == l, self.flow)
                for n in conn_nodes:
                    i = n[0]
                    s = NodeInputKillGen(i, nodes[i - 1].kill, nodes[i - 1].gen)
                    input.append(s)
                c = UnionConstraint(l, input)
                constraints.append(c)

        return constraints


class ReachingDefinitionsAnalyzer(BitVectorAnalyzerBase):

    def __init__(self, program):
        super(ReachingDefinitionsAnalyzer, self).__init__(program)
        self.assigns = self.assignments(self.nodes)
        self.base_set = set(map(lambda l: (l[0], '?'), program.variables()))

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

    def setKillGenSets(self, nodes):
        for node in nodes:
            # Find kill and gen
            if type(node) is McAssignment:
                # Lhs of assignment will be variable, record or array. Handled by the variables-method,
                # which returns set of variables in expression.
                variables = node.lhs.variables()
                self.setNodeKillGen(node, variables, self.assigns)
            elif type(node) is McReadStatement:
                variables = node.variables()
                self.setNodeKillGen(node, variables, self.assigns)

    def setNodeKillGen(self, node, variables, assignments):
        kill = set(filter(lambda a: a[0] in variables, assignments)) | set(map(lambda v: (v, '?'), variables))
        gen = set(map(lambda v: (v, node.init), variables))
        node.kill, node.gen = kill, gen


class LiveVariablesAnalyzer(BitVectorAnalyzerBase):
    def __init__(self, program):
        super(LiveVariablesAnalyzer, self).__init__(program)
        self.flow = set(map(lambda f: (f[1], f[0]), program.flow()))
        self.base_case = [len(self.nodes)]
        self.base_set = set()

    def setKillGenSets(self, nodes):
        for node in nodes:
            # Find kill and gen
            if type(node) is McAssignment:
                # Lhs of assignment will be variable, record or array. Handled by the variables-method,
                # which returns set of variables in expression.
                node.kill = node.lhs.variables()
                node.gen = node.rhs.variables()
            elif type(node) is McReadStatement:
                node.kill = node.variables()
            elif type(node) is McWhileStatement or type(node) is McIfStatement or type(node) is McIfElseStatement:
                node.gen = node.condition.variables()
            else:
                node.gen = node.variables()
