from microc.statements import McAssignment
from microc.statements import McReadStatement
from microc.statements import McIfStatement
from microc.statements import McIfElseStatement
from microc.statements import McWhileStatement
from microc.operations import McDivisionOp
from microc.operations import McMinusOp
from microc.operations import McPlusOp
from microc.operations import McMultiplyOp
from microc.operations import McRemainderOp
from microc.expressions import McValueLiteral
from microc.expressions import McVariable
from analysis.data import UnionConstraint
from analysis.data import NodeInputSet
from analysis.data import NodeInputKillGen


class ReachingDefinitionsAnalyzer:

    def analyze(self, program):
        nodes = program.nodeList()
        variables = program.variables()
        flow = program.flow()
        assignments = self.assignments(nodes)

        self.setKillGenSets(nodes, assignments)
        return self.constructConstraints(nodes, variables, flow)

    # Returns the list of assignments in nodes of the program. Needed to define kill and gen sets.
    def assignments(self, nodes):
        assignments = set()
        for node in nodes:
            if type(node) is McAssignment:
                variables = node.lhs.variables()
                assignments = assignments | set(map(lambda v: (v, node.init), variables))
            elif type(node) is McReadStatement:
                variables = node.variables()
                assignments = assignments | set(map(lambda v: (v, node.init), variables))

        return assignments

    def setKillGenSets(self, nodes, assignments):
        for node in nodes:
            # Find kill and gen
            if type(node) is McAssignment:
                # Lhs of assignment will be variable, record or array. Handled by the variables-method,
                # which returns set of variables in expression.
                variables = node.lhs.variables()
                self.setNodeKillGen(node, variables, assignments)
            elif type(node) is McReadStatement:
                variables = node.variables()
                self.setNodeKillGen(node, variables, assignments)

    def setNodeKillGen(self, node, variables, assignments):
        kill = set(filter(lambda a: a[0] in variables, assignments)) | set(map(lambda v: (v, '?'), variables))
        gen = set(map(lambda v: (v, node.init), variables))
        node.kill, node.gen = kill, gen

    def constructConstraints(self, nodes, variables, flow):
        constraints = []
        for node in nodes:
            l = node.init
            if l == 1:
                base_set = set(map(lambda l: (l[0], '?'), variables))
                c = UnionConstraint(l, [NodeInputSet(l, base_set)])
                constraints.append(c)
            else:
                input = []
                conn_nodes = filter(lambda f: f[1] == l, flow)
                for n in conn_nodes:
                    i = n[0]
                    s = NodeInputKillGen(i, nodes[i-1].kill, nodes[i-1].gen)
                    input.append(s)
                c = UnionConstraint(l, input)
                constraints.append(c)

        return constraints


class DetectingSignsAnalyser:

    #Check for possible flows that enter the current node

    def assignments(self, nodes, initialSigns):
        #Typer assignment + read + if + while
        signs = []
        initial = initialSigns
        count = 0
        signs.append([count, initial])
        for node in nodes:
            current = {}
            count += 1
            #ASSIGNMENT
            if type(node) == McAssignment:
                rhsType = type(node.rhs)
                lhsVariable = node.lhs.variables().pop()
                #MINUS
                if rhsType == McMinusOp:
                    #Only use lefthand side for signdetection
                    minusOp = node.rhs
                    OpLhsType = type(minusOp.lhs)
                    if OpLhsType == McValueLiteral:
                        OpLhsValue = minusOp.lhs
                        if OpLhsValue > 0:
                            current[lhsVariable] = ['+', '0', '-']
                        elif OpLhsValue == 0:
                            current[lhsVariable] = ['0', '-']
                        elif OpLhsValue < 0:
                            current[lhsVariable] = ['-']
                    elif len(minusOp.lhs.variables()) > 0:
                        innerLhsVariable = minusOp.lhs.variables().pop()
                        current[lhsVariable] = signs[count-1][1][innerLhsVariable]
                    current[lhsVariable] = ['+','0','-']
                #PLUS    
                elif rhsType == McPlusOp:
                    #Getting the plus operation
                    plusOp = node.rhs
                    #Getting type of input for lhs
                    OpLhsType = type(plusOp.lhs)
                    #Getting type of input for rhs
                    OpRhsType = type(plusOp.rhs)

                    if OpLhsType == McValueLiteral and OpRhsType == McValueLiteral:
                        #Values of input lhs and rhs
                        OpLhsVal = plusOp.lhs
                        OpRhsVal = plusOp.rhs
                        if OpLhsVal > 0:
                            if OpRhsVal >= 0 :
                                current[lhsVariable] = ['+']
                            elif OpRhsVal < 0: 
                                current[lhsVariable] = ['+','0','-']
                        elif OpLhsVal == 0:
                            if OpRhsVal < 0: 
                                current[lhsVariable] = ['-']
                            elif OpRhsVal == 0: 
                                current[lhsVariable] = ['0']
                            elif OpRhsVal > 0:
                                current[lhsVariable] = ['+']
                        elif OpLhsVal < 0:
                            if OpRhsVal <= 0:
                                current[lhsVariable] = ['-']
                            elif OpRhsVal > 0:
                                current[lhsVariable] = ['+','0','-']
                    elif len(plusOp.lhs.variables()) > 0 and len(plusOp.rhs.variables()) > 0:   
                        current[lhsVariable] = list(set(signs[count-1][1][plusOp.lhs.variables().pop()]) & set(signs[count-1][1][plusOp.rhs.variables().pop()]))
                    else: 
                        current[node.lhs] = ['+','0','-']

                #MULTIPLICATION todo
                elif rhsType == McMultiplyOp:
                    multiOp = node.rhs
                    OpLhsType = type(multiOp.lhs)
                    OpRhsType = type(multiOp.rhs)

                    if OpLhsType == McValueLiteral and OpRhsType == McValueLiteral:
                        OplhsVal = multiOp.lhs
                        OprhsVal = multiOp.rhs

                        if OplhsVal == 0 or OprhsVal == 0:
                            current[lhsVariable] = ['0']
                        if OplhsVal > 0:
                            if OprhsVal > 0:
                                current[lhsVariable] = ['+']
                            elif OprhsVal < 0:
                                current[lhsVariable] = ['-']
                        if OplhsVal < 0:
                            if OprhsVal > 0:
                                current[lhsVariable] = ['-']
                            elif  OprhsVal < 0:
                                current[lhsVariable] = ['+']
                    elif len(multiOp.lhs.variables()) > 0 and len(multiOp.rhs.variables()) > 0:
                        current[lhsVariable] = list (set(signs[count-1][1][multiOp.lhs.variables().pop()]) & set(signs[count-1][1][multiOp.rhs.variables().pop()]))
                    else:
                        current[node.lhs] = signs[count-1][1][node.lhs]
                #DIVISION    todo
                elif rhsType == McDivisionOp:
                    diviOp = node.rhs
                    OpLhsType = type(diviOp.lhs)
                    OpRhsType = type(diviOp.rhs)

                    if OpLhsType == McValueLiteral and OpRhsType == McValueLiteral:
                        OpLhsVal = diviOp.lhs
                        OpRhsVal = diviOp.rhs

                        if OpLhsVal == 0:
                            current[lhsVariable] = ['0']
                        elif OpLhsVal > 0:
                            if OpRhsVal < 0:
                                current[lhsVariable] = ['0','-']
                            elif OpRhsVal > 0:
                                current[lhsVariable] = ['+', '0']
                        elif OpLhsVal < 0:
                            if OpRhsVal < 0:
                                current[lhsVariable] = ['+','0']
                            elif OpRhsVal > 0:
                                current[lhsVariable] = ['0','-']
                    elif len(diviOp.lhs.variables()) > 0 and len(diviOp.rhs.variables()) > 0:
                        current[lhsVariable] = list(set(signs[count-1][1][diviOp.lhs.variables().pop()]) & set(signs[count-1][1][diviOp.rhs.variables().pop()]))
                    else:
                        current[lhsVariable] = signs[count-1][1][node.lhs]
                #REMAINDER    todo
                elif rhsType == McRemainderOp:
                    current[lhsVariable] = ['+','0']
                #LITERAL    todo
                elif rhsType == McValueLiteral:
                    if int(node.rhs.value) > 0:
                        current[lhsVariable] = ['+']
                    elif int(node.rhs.value) == 0:
                        current[lhsVariable] = ['0']
                    else:
                        current[lhsVariable] = ['-']
            #READ todo
            elif type(node) == McReadStatement:
                current[lhsVariable] = ['+','0','-']
            #IF   todo 
            elif type(node) == McIfStatement:
                current[lhsVariable] = ['+','0','-']
            #IFELSE  todo
            elif type(node) == McIfElseStatement:
                current[lhsVariable] = ['+','0','-']
            #WHILE
            elif type(node) == McWhileStatement:
                current[lhsVariable] = ['+','0','-']
            #INSERTION OF PREVIOUS SIGNS    
            for i in signs[count-1][1]:
                if i not in current:
                    current[i] = signs[count-1][1][i]
            #current.sort
            signs.append([count, current])
        return signs

    #Function that detects the sign of a variable 

    #Function that calculates the sign of an operation
    
    def analyse(self, program, initialSigns):
        nodes = program.nodeList()
        return self.assignments(nodes, initialSigns)