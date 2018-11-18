from analysis.data import Constraint

class WorklistBase:
    def __init__(self, program):
        self.program, self.flow, self.nodes, self.variables = program, program.flow(), program.nodeList(), program.variables()

    def computeSolution(self, constraints):
        w, analysis, infl = [], [], []

        for c in constraints:
            w = self.insert(c, w)
            analysis.append(set())
            infl.append(set())

        # TODO: Make data structure for constraints.
        #for c in constraints:
            #for x in fv(rhs):
                #infl[x] = infl[x] | c

        while w != self.equal:
            c, w = self.extract(w)
            # TODO: Set new
            new = set()
            if not analysis[c] >= new:
                analysis[c.x-1] = analysis[c.x-1] | new
                for cp in infl[c]:
                    w = self.insert(cp, w)

        return analysis


class WorklistChaotic(WorklistBase):
    def __init__(self):
        self.empty = []

    def insert(self, c, w):
        w.append(c)
        return list(set(w))

    def extract(self, w):
        c = w.pop(0)
        return c, w



