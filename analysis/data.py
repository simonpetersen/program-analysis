# Representation of an equation of the form x >= t. Example: x1 >= x2 U (x3\S34) U S3
class Constraint:
    def __init__(self, x, t):
        self.x, self.t = x, t


# Base class for the set that gets returned from an action.
class PostActionBase:
    def __init__(self, i):
        self.i = i


class PostActionSet(PostActionBase):
    def __init__(self, i, s):
        super(PostActionSet, self).__init__(i)
        self.s = s


# Represents the set that gets returned from an action.
class PostActionKillGen(PostActionBase):
    def __init__(self, i, kill, gen):
        super(PostActionKillGen, self).__init__(i)
        self.kill, self.gen = kill, gen
