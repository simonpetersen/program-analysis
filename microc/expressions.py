from microc.microc import McNode


class McVariableDeclaration(McNode):
    def __init__(self, l, variable):
        super(McVariableDeclaration, self).__init__(l)
        self.variable = variable

    def variables(self):
        return set(self.variable)


class McVariable(McNode):
    def __init__(self, l, variable):
        super(McVariable, self).__init__(l)
        self.variable = variable

    def variables(self):
        return set(self.variable)


class McArrayDeclaration(McNode):
    def __init__(self, l, variable, size):
        super(McArrayDeclaration, self).__init__(l)
        self.variable, self.size = variable, size

    def variables(self):
        return set(self.variable)


class McArrayAccessor(McNode):
    def __init__(self, l, array, index):
        super(McArrayAccessor, self).__init__(l)
        self.array, self.index = array, index

    def variables(self):
        return set(self.array)


class McRecordDeclaration(McNode):
    def __init__(self, l, record, elements):
        super(McRecordDeclaration, self).__init__(l)
        self.record, self.elements = record, elements

    def variables(self):
        return set(self.record)


class McRecordAccessor(McNode):
    def __init__(self, l, record, element):
        super(McRecordAccessor, self).__init__(l)
        self.record, self.element = record, element

    # Returns the record as variable.
    def variables(self):
        return set(self.record)


class McValueLiteral(McNode):
    def __init__(self, l, value):
        super(McValueLiteral, self).__init__(l)
        self.value = value
