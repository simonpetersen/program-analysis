from microc.microc import McNode
from microc.microc import McBinaryExpression


class McWhileStatement(McNode):
    def __init__(self, l, condition, body):
        super(McWhileStatement, self).__init__(l)
        self.condition, self.body = condition, body

    # Returns the nodes in the flow graph of the while statement.
    def flow(self):
        if len(self.body) == 0:
            return set()

        s = {(self.init, self.body[0].init)}
        for i in range(0, len(self.body)):
            if i == len(self.body) - 1:
                for l in self.body[i].final:
                    s = s | {(l, self.init)}
            else:
                for l in self.body[i].final:
                    s = s | {(l, self.body[i+1].init)}
            s = s | self.body[i].flow()

        return s

    def variables(self):
        s = self.condition.variables()
        for node in self.body:
            s = s | node.variables()

        return s


class McIfStatement(McNode):
    def __init__(self, l, condition, body):
        super(McIfStatement, self).__init__(l)
        self._condition, self._body = condition, body
        if len(self._body) > 0:
            self._final = [self.body[-1].init]

    # Returns the nodes in the flow graph of the if statement.
    def flow(self):
        if len(self.body) == 0:
            return set()

        s = {(self.l, self.body[0].init)}
        for i in range(0, len(self.body)-1):
            for l in self.body[i].final:
                s = s | {(l, self.body[i + 1].init)}
            s = s | self.body[i].flow()

        return s

    def variables(self):
        s = self.condition.variables()
        for node in self.body:
            s = s | node.variables()

        return s


class McIfElseStatement(McNode):
    def __init__(self, l, condition, thenBody, elseBody):
        super(McIfStatement, self).__init__(l)
        self.condition, self.thenBody, self.elseBody, self.body = condition, thenBody, elseBody, thenBody + elseBody
        if len(self.thenBody) > 0:
            self.final = [self.thenBody[-1].init]
        if len(self.elseBody) > 0:
            self.final.append(self.elseBody[-1].init)

    # Returns the nodes in the flow graph of the if-else statement.
    def flow(self):
        s = set()
        if len(self.thenBody) > 0:
            s = s |{(self.l, self.thenBody[0].init)}
            for i in range(0, len(self.thenBody) - 1):
                for l in self.thenBody[i].final:
                    s = s | {(l, self.thenBody[i + 1].init)}
                s = s | self.thenBody[i].flow()

        if len(self.elseBody) > 0:
            s = s |{(self.l, self.elseBody[0].init)}
            for i in range(0, len(self.elseBody) - 1):
                for l in self.elseBody[i].final:
                    s = s | {(l, self.elseBody[i + 1].init)}
                s = s | self.elseBody[i].flow()

        return s

    def variables(self):
        s = self.condition.variables()
        for node in self.thenBody:
            s = s | node.variables()

        for node in self.elseBody:
            s = s | node.variables()

        return s


class McAssignment(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McAssignment, self).__init__(l, lhs, rhs)
