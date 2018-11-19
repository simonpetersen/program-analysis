from microc.microc import McProgram
import microc.statements
import microc.expressions
import microc.operations


class ParserMicroC:

    def __init__(self, program):
        self.lines = program.split("\n")
        self.tokens = program.split()
        self.l = 1

    # Parse method, taking a micro-c program as string parameter.
    def parse(self):
        nodes = self.block()
        program = McProgram(nodes)
        return program

    def checkForLineEnd(self):
        if self.tokens[0][-1] == ';' and len(self.tokens[0]) > 1:
            # I.e: x; remove ; from x;-token, and add separately
            self.tokens[0] = self.tokens[0][:-1]
            self.tokens.insert(1, ';')
        if self.tokens[0] == ';':
            self.l += 1
            self.tokens.pop(0)

    def nextToken(self):
        self.checkForLineEnd()
        return self.tokens.pop(0)

    # Checks if the next token is expected token.
    def mustBe(self, token):
        self.checkForLineEnd()
        if not self.nextTokenIs(token):
            next_token = self.tokens[0]
            print('Syntax error. %s found when %s expected.' % (next_token, token))

    # Checks the next token, and only removes it, if it matches
    def nextTokenIs(self, token):
        if token != ';':
            self.checkForLineEnd()
        if self.tokens[0] == token:
            self.tokens.pop(0)
            return True
        if len(self.tokens[0]) >= len(token):
            if self.tokens[0][:len(token)] == token:
                self.tokens[0] = self.tokens[0][len(token):]
                return True
        return False

    def getVariableName(self):
        variable = ""
        i = 0
        word = self.tokens[0]
        while i < len(word):
            c = word[i]
            if c.isalpha():
                variable += c
                i += 1
            else:
                self.tokens[0] = word[i:]
                return variable
        self.tokens.pop(0)
        return variable

    def statement(self):
        if self.nextTokenIs('while'):
            return self.parseWhile()
        elif self.nextTokenIs('if'):
            return self.parseIf()
        elif self.nextTokenIs('read'):
            statement = self.statement()
            return microc.statements.McReadStatement(self.l, statement)
        elif self.nextTokenIs('write'):
            statement = self.statement()
            return microc.statements.McWriteStatement(self.l, statement)
        else:
            return self.expression()

    def parseWhile(self):
        l = self.l
        self.mustBe('(')
        condition = self.expression()
        self.mustBe(')')
        body = self.block()
        return microc.statements.McWhileStatement(l, condition, body)

    def parseIf(self):
        l = self.l
        self.mustBe('(')
        condition = self.expression()
        self.mustBe(')')
        body = self.block()
        if self.nextTokenIs('else'):
            else_body = self.block()
            return microc.statements.McIfElseStatement(l, condition, body, else_body)
        return microc.statements.McIfStatement(l, condition, body)

    # Returns a list of statements
    def block(self):
        statements = []
        self.mustBe('{')
        while not self.nextTokenIs('}'):
            s = self.statement()
            statements.append(s)
        return statements

    def expression(self):
        l = self.l
        lhs = self.logicalExpression()
        if self.nextTokenIs(':='):
            rhs = self.logicalExpression()
            return microc.statements.McAssignment(l, lhs, rhs)
        return lhs

    def logicalExpression(self):
        l = self.l
        lhs = self.relationalExpression()
        if self.nextTokenIs('|'):
            rhs = self.relationalExpression()
            return microc.operations.McLogicalOrOp(l, lhs, rhs)
        elif self.nextTokenIs('&'):
            rhs = self.relationalExpression()
            return microc.operations.McLogicalAndOp(l, lhs, rhs)
        return lhs

    def relationalExpression(self):
        l = self.l
        lhs = self.additiveExpression()
        if self.nextTokenIs('=='):
            rhs = self.additiveExpression()
            return microc.operations.McEqualsOp(l, lhs, rhs)
        elif self.nextTokenIs('!='):
            rhs = self.additiveExpression()
            return microc.operations.McNotEqualsOp(l, lhs, rhs)
        elif self.nextTokenIs('>'):
            rhs = self.additiveExpression()
            return microc.operations.McGreaterOp(l, lhs, rhs)
        elif self.nextTokenIs('>='):
            rhs = self.additiveExpression()
            return microc.operations.McGreaterEqualsOp(l, lhs, rhs)
        elif self.nextTokenIs('<'):
            rhs = self.additiveExpression()
            return microc.operations.McLessOp(l, lhs, rhs)
        elif self.nextTokenIs('<='):
            rhs = self.additiveExpression()
            return microc.operations.McLessEqualsOp(l, lhs, rhs)
        return lhs

    def additiveExpression(self):
        l = self.l
        lhs = self.multiplicativeExpression()
        more = True
        while more:
            if self.nextTokenIs('+'):
                lhs = microc.operations.McPlusOp(l, lhs, self.multiplicativeExpression())
            elif self.nextTokenIs('-'):
                lhs = microc.operations.McMinusOp(l, lhs, self.multiplicativeExpression())
            else:
                more = False
        return lhs

    def multiplicativeExpression(self):
        l = self.l
        lhs = self.negateExpression()
        # Loop is needed, in case of a*b*c
        more = True
        while more:
            if self.nextTokenIs('*'):
                lhs = microc.operations.McMultiplyOp(l, lhs, self.negateExpression())
            elif self.nextTokenIs('/'):
                lhs = microc.operations.McDivisionOp(l, lhs, self.negateExpression())
            elif self.nextTokenIs('%'):
                lhs = microc.operations.McRemainderOp(l, lhs, self.negateExpression())
            else:
                more = False
        return lhs

    def negateExpression(self):
        l = self.l
        if self.nextTokenIs('not'):
            expression = self.logicalExpression()
            return microc.expressions.McNotExpression(l, expression)
        return self.variable()

    def variable(self):
        l = self.l
        variable = self.getVariableName()
        if variable == 'int':
            if self.nextTokenIs('['):
                value = self.parseValueLiteral()
                self.mustBe(']')
                variable = self.getVariableName()
                return microc.expressions.McArrayDeclaration(l, variable, value)
            variable = self.getVariableName()
            return microc.expressions.McVariableDeclaration(l, variable)
        elif not variable:
            if self.nextTokenIs('{'):
                elements = []
                while not self.nextTokenIs('}'):
                    self.mustBe('int')
                    variable = self.getVariableName()
                    elements.append(variable)
                    self.nextTokenIs(';')
                variable = self.getVariableName()
                return microc.expressions.McRecordDeclaration(l, variable, elements)
            # Must be value literal
            return self.parseValueLiteral()
        if self.nextTokenIs('.'):
            element = self.getVariableName()
            return microc.expressions.McRecordAccessor(l, variable, element)
        elif self.nextTokenIs('['):
            accessor = self.getVariableName()
            if not accessor:
                # must be a integer literal as accessor.
                accessor = self.nextToken()
            self.mustBe(']')
            return microc.expressions.McArrayAccessor(l, variable, accessor)
        return microc.expressions.McVariable(l, variable)


    def parseValueLiteral(self):
        token = self.nextToken()
        return microc.expressions.McValueLiteral(self.l, token)
