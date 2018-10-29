from microc.microc import McBinaryExpression


class McPlusOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McPlusOp, self).__init__(l, lhs, rhs)


class McMinusOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McMinusOp, self).__init__(l, lhs, rhs)


class McMultiplyOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McMultiplyOp, self).__init__(l, lhs, rhs)


class McGreaterThanOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McGreaterThanOp, self).__init__(l, lhs, rhs)

