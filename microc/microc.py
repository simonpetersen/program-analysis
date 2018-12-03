class McProgram:
    def __init__(self, nodes):
        self.nodes = nodes

    # Returns the edges in the flow graph representing the program.
    def flow(self):
        s = set()
        for i in range(0, len(self.nodes)-1):
            if i < len(self.nodes)-1:
                for l in self.nodes[i].final:
                    s = s | {(l, self.nodes[i+1].init)}
            s = s | self.nodes[i].flow()

        return s

    # Returns the set of variables present in the program.
    def variables(self):
        s = set()
        for node in self.nodes:
            s = s | node.variables()

        return s

    # Returns all the nodes in the program in a list.
    def nodeList(self):
        return self.subnodes(self.nodes)

    def subnodes(self, nodes):
        node_list = []
        for node in nodes:
            node_list.append(node)
            if hasattr(node, "body"):
                node_list.extend(self.subnodes(node.body))
        return node_list


class McNode:
    def __init__(self, l):
        self.init, self.final = l, [l]
        # Init kill and gen as empty sets
        self.kill, self.gen = set(), set()

    def flow(self):
        return set()

    def variables(self):
        return set()


class McBinaryExpression(McNode):
    def __init__(self, l, lhs, rhs):
        super(McBinaryExpression, self).__init__(l)
        self.lhs, self.rhs = lhs, rhs

    def variables(self):
        return self.lhs.variables() | self.rhs.variables()


class McStatement(McNode):
    def __init__(self, l):
        super(McStatement, self).__init__(l)