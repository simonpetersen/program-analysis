from microc.microc import McNode


class McVariable(McNode):
    def __init__(self, l, variable):
        super(McVariable, self).__init__(l)
        self.variable = variable

    def variables(self):
        return set(self.variable)


class McValueLiteral(McNode):
    def __init__(self, l, value):
        super(McValueLiteral, self).__init__(l)
        self.value = value
