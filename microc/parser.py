from microc.microc import McProgram


class ParserMicroC:

    def __init__(self, program):
        self.lines = program.split("\n")

    # Parse method, taking a micro-c program as string parameter.
    def parse(self):
        nodes = []

        while self.lines:
            # Get the next element in the list
            line = self.lines.pop(0)
            self.parseLine(line)

        program = McProgram(nodes)
        return program

    def parseLine(self, line):
        line.strip()
        tokens = line.split()
        print(tokens)
        first = tokens[0]
        if first == 'while':
            self.parseWhile()
        elif first == "if":
            self.parseIf()

    def parseWhile(self):
        pass

    def parseIf(self):
        pass

