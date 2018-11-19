class WorklistBase:
    def __init__(self):
        self.empty = []

    def computeSolution(self, constraints):
        w, analysis, infl = [], [], []

        for c in constraints:
            w = self.insert(c, w)
            analysis.append(set())
            infl.append(set())

        for c in constraints:
            for x in c.t:
                infl[x.i-1] = infl[x.i-1] | {c}

        while w != self.empty:
            c, w = self.extract(w)
            new = self.eval(c, analysis)
            if not analysis[c.x-1] >= new:
                analysis[c.x-1] = analysis[c.x-1] | new
                for cp in infl[c.x-1]:
                    w = self.insert(cp, w)

        return analysis

    def eval(self, constraint, analysis):
        new = set()
        for s in constraint.t:
            result = s.result(analysis[s.i-1])
            new = constraint.func(result, new)
        return new


class WorklistChaotic(WorklistBase):
    def insert(self, c, w):
        w.append(c)
        return list(set(w))

    def extract(self, w):
        c = w.pop(0)
        return c, w


class WorklistFifo(WorklistBase):
    def insert(self, c, w):
        w.append(c)
        return w

    def extract(self, w):
        c = w[0]
        return c, w[1:]


class WorklistLifo(WorklistBase):
    def insert(self, c, w):
        w.append(c)
        return w

    def extract(self, w):
        c = w[-1]
        return c, w[:-1]



