from analysis.analyzer import ReachingDefinitionsAnalyzer
import microc.expressions
import microc.statements
import microc.microc
import microc.operations


'''
x := 5
y := 1
while (x > 1) {
    y := x * y
    x := x - 1
}
x := 0
'''

# Init variables
x = microc.expressions.McVariable(1, "x")
y = microc.expressions.McVariable(2, "y")
nodes = [microc.statements.McAssignment(1, x, microc.expressions.McValueLiteral(1, "5"))]
nodes.append(microc.statements.McAssignment(2, y, microc.expressions.McValueLiteral(2, "1")))
# Init content of while-statement
condition = microc.operations.McGreaterThanOp(3, x, microc.expressions.McValueLiteral(3, "1"))
y_assignment = microc.statements.McAssignment(4, y, microc.operations.McMultiplyOp(4, x, y))
x_assignment = microc.statements.McAssignment(5, x, microc.operations.McMinusOp(5, x, microc.expressions.McValueLiteral(5, "1")))
# Append while-statement
nodes.append(microc.statements.McWhileStatement(3, condition, [y_assignment, x_assignment]))
# Append finale assignment to x
nodes.append(microc.statements.McAssignment(6, x, microc.expressions.McValueLiteral(6, "1")))

program = microc.microc.McProgram(nodes)

analyzer = ReachingDefinitionsAnalyzer()
constraints = analyzer.analyze(program)

for c in constraints:
    print(c)

# Should be changed when Worklist is implemented.
#wl = ReachingDefinitionsWorklist(program)
#rd_in, rd_out = wl.computeSolution()
