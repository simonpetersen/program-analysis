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

    # Checks if the next token is expected token.
    def mustBe(self, token):
        self.checkForLineEnd()
        if not self.nextTokenIs(token):
            next_token = self.tokens[0]
            print('Syntax error. %s found when %s expected.' % (next_token, token))

    # Checks the next token, and only removes it, if it matches
    def nextTokenIs(self, token):
        self.checkForLineEnd()
        if self.tokens[0] == token:
            self.tokens.pop(0)
            return True
        if len(self.tokens[0]) >= len(token):
            if self.tokens[0][:len(token)] == token:
                self.tokens[0] = self.tokens[len(token):]
                return True
        return False

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
        self.mustBe('(')
        condition = self.expression()
        self.mustBe(')')
        body = self.block()
        return microc.statements.McWhileStatement(self.l, condition, body)

    def parseIf(self):
        self.mustBe('(')
        condition = self.expression()
        self.mustBe(')')
        body = self.block()
        if self.nextTokenIs('else'):
            else_body = self.block()
            return microc.statements.McIfElseStatement(self.l, condition, body, else_body)
        return microc.statements.McIfStatement(self.l, condition, body)

    # Returns a list of statements
    def block(self):
        statements = []
        self.mustBe('{')
        while not self.nextTokenIs('}'):
            s = self.statement()
            statements.append(s)
        return statements

    def expression(self):
        lhs = self.logicalExpression()
        if self.nextTokenIs(':='):
            rhs = self.logicalExpression()
            return microc.statements.McAssignment(self.l, lhs, rhs)
        return lhs

    def logicalExpression(self):
        lhs = self.relationalExpression()
        if self.nextTokenIs('|'):
            rhs = self.relationalExpression()
            return microc.operations.McLogicalOrOp(self.l, lhs, rhs)
        elif self.nextTokenIs('&'):
            rhs = self.relationalExpression()
            return microc.operations.McLogicalAndOp(self.l, lhs, rhs)
        return lhs

    def relationalExpression(self):
        lhs = self.additiveExpression()
        if self.nextTokenIs('=='):
            rhs = self.additiveExpression()
            return microc.operations.McEqualsOp(self.l, lhs, rhs)
        elif self.nextTokenIs('!='):
            rhs = self.additiveExpression()
            return microc.operations.McNotEqualsOp(self.l, lhs, rhs)
        elif self.nextTokenIs('>'):
            rhs = self.additiveExpression()
            return microc.operations.McGreaterOp(self.l, lhs, rhs)
        elif self.nextTokenIs('>='):
            rhs = self.additiveExpression()
            return microc.operations.McGreaterEqualsOp(self.l, lhs, rhs)
        elif self.nextTokenIs('<'):
            rhs = self.additiveExpression()
            return microc.operations.McLessOp(self.l, lhs, rhs)
        elif self.nextTokenIs('<='):
            rhs = self.additiveExpression()
            return microc.operations.McLessEqualsOp(self.l, lhs, rhs)
        return lhs

    def additiveExpression(self):
        lhs = self.multiplicativeExpression()
        more = True
        while more:
            if self.nextTokenIs('+'):
                lhs = microc.operations.McPlusOp(self.l, lhs, self.multiplicativeExpression())
            elif self.nextTokenIs('-'):
                lhs = microc.operations.McMinusOp(self.l, lhs, self.multiplicativeExpression())
            else:
                more = False
        return lhs

    def multiplicativeExpression(self):
        lhs = self.negateExpression()
        # Loop is needed, in case of a*b*c
        more = True
        while more:
            if self.nextTokenIs('*'):
                lhs = microc.operations.McMultiplyOp(self.l, lhs, self.negateExpression())
            elif self.nextTokenIs('/'):
                lhs = microc.operations.McDivisionOp(self.l, lhs, self.negateExpression())
            elif self.nextTokenIs('%'):
                lhs = microc.operations.McRemainderOp(self.l, lhs, self.negateExpression())
            else:
                more = False
        return lhs

    def negateExpression(self):
        if self.nextTokenIs('not'):
            expression = self.logicalExpression()
            return microc.expressions.McNotExpression(self.l, expression)
        return self.variable()

    # TODO: Fix
    def variable(self):
        token = self.tokens.pop(0)
        return microc.expressions.McVariable(self.l, token)

