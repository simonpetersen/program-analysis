from microc.microc import McBinaryExpression
from microc.microc import McExpression


class McPlusOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McPlusOp, self).__init__(l, lhs, rhs)


class McMinusOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McMinusOp, self).__init__(l, lhs, rhs)


class McMultiplyOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McMultiplyOp, self).__init__(l, lhs, rhs)


class McDivisionOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McDivisionOp, self).__init__(l, lhs, rhs)


class McRemainderOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McRemainderOp, self).__init__(l, lhs, rhs)


# Operation: v1 == v2
class McEqualsOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McEqualsOp, self).__init__(l, lhs, rhs)


# Operation: v1 != v2
class McNotEqualsOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McNotEqualsOp, self).__init__(l, lhs, rhs)


# Operation: lhs > rhs
class McGreaterOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McGreaterOp, self).__init__(l, lhs, rhs)


# Operation: lhs >= rhs
class McGreaterEqualsOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McGreaterEqualsOp, self).__init__(l, lhs, rhs)


# Operation: lhs < rhs
class McLessOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McLessOp, self).__init__(l, lhs, rhs)


# Operation: lhs <= rhs
class McLessEqualsOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McLessEqualsOp, self).__init__(l, lhs, rhs)


# Operation: lhs | rhs
class McLogicalOrOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McLogicalOrOp, self).__init__(l, lhs, rhs)


# Operation: lhs & rhs
class McLogicalAndOp(McBinaryExpression):
    def __init__(self, l, lhs, rhs):
        super(McLogicalAndOp, self).__init__(l, lhs, rhs)


# Operation: not b
class McNotExpression(McExpression):
    def __index__(self, l, expression):
        super(McNotExpression, self).__init__(l)
        self.expression = expression

    def variables(self):
        return self.expression.variables()