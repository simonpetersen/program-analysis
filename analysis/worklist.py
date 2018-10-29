class Worklist:
    def __init__(self, program):
        self.program, self.flow, self.nodes, self.variables = program, program.flow(), program.nodeList(), program.variables()

    def computeSolution(self):
        w, in_sets, out_sets = self.flow.copy(), {}, {}

        for node in self.nodes:
            l = node.init
            in_sets[l] = self.base_value if l in self.base_set else set()

        while w:
            el = w.pop()
            l, lp = el[0], el[1]
            out = (in_sets[l] - self.nodes[l-1].kill) | self.nodes[l-1].gen

            if not out <= in_sets[lp]:
                in_sets[lp] = self.join_func(in_sets[lp], out)

                for s in self.flow:
                    if lp == s[0]:
                        w = w | {s}
        for i in in_sets:
            out_sets[i] = (in_sets[i] - self.nodes[i-1].kill) | self.nodes[i-1].gen

        return in_sets, out_sets


class ReachingDefinitionsWorklist(Worklist):
    def __init__(self, program):
        super(ReachingDefinitionsWorklist, self).__init__(program)
        self.base_set = {1}
        self.base_value = set(map(lambda l: (l[0],'?'), self.variables))
        self.join_func = lambda in_set, out_set: in_set | out_set


class LiveVariablesWorklist(Worklist):
    def __init__(self, program):
        super(LiveVariablesWorklist, self).__init__(program)
        self.base_set = set(self.program.nodes[-1].final)
        self.base_value = self.variables
        self.join_func = lambda in_set, out_set: in_set | out_set
        # Flow-edges should be reversed, because of backward analysis
        self.flow = set(map(lambda l: (l[1], l[0]), self.flow))
