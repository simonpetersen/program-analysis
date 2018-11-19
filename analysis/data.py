from abc import ABC, abstractmethod


# Representation of an equation of the form x >= t. Example: x1 >= x2 U (x3\S34) U S3
# t is a list of NodeInputBase objects.
class Constraint:
    def __init__(self, x, t):
        self.x, self.t = x, t


class UnionConstraint(Constraint):
    def __init__(self, x, t):
        super(UnionConstraint, self).__init__(x,t)
        self.func = lambda s1, s2: s1 | s2

# Abstract base class for the set that is passed as input to a node.
class NodeInputBase(ABC):
    def __init__(self, i):
        self.i = i

    @abstractmethod
    def result(self, s):
        pass


# The result of an action that only returns a set. Used for the input to an initial node in a program.
class NodeInputSet(NodeInputBase):
    def __init__(self, i, s):
        super(NodeInputSet, self).__init__(i)
        self.s = s

    def result(self, s):
        return self.s


# Representation of a set of the form: (xi \ kill) U gen. i is an integer representing the label of the node.
class NodeInputKillGen(NodeInputBase):
    def __init__(self, i, kill, gen):
        super(NodeInputKillGen, self).__init__(i)
        self.kill, self.gen = kill, gen

    def result(self, s):
        if not self.kill and not self.gen:
            return s
        return (s - self.kill) | self.gen
