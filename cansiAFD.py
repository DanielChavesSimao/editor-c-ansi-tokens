from ctoken import CToken

class CansiAFD:

    keywordsHash = {
        2: ['do', 'if'],
        3: ['int', 'for'],
        4: ['auto', 'else', 'long', 'case', 'enum', 'char', 'void', 'goto'],
        5: ['break', 'union', 'const', 'float', 'short', 'while'],
        6: ['double', 'struct', 'switch', 'extern', 'return', 'signed', 'sizeof', 'static'],
        7: ['typedef', 'default'],
        8: ['register', 'unsigned', 'continue', 'volatile']
    }

    def __init__(self, sentenca: str) -> None:
        self.col = 0
        self.tokens = []
        self.sentenca = sentenca
        self.palavraAuxiliar = ""
        self.verificado = False
        self.palavrasReservadas = [
            "auto", "break", "case", "char", "const", "continue",
            "default", "do", "double", "else", "enum", "extern",
            "float", "for", "goto", "if", "inline", "int", "long",
            "register", "restrict", "return", "short", "while",
            "signed", "static", "struct", "switch", "typedef",
            "union", "void", "volatile", "while"
        ]

    def calcularIndex1(self):
        return f'{self.lineNumber}.{self.col - 1 - len(self.palavraAuxiliar)}'

    def calcularIndex2(self):
        return f'{self.lineNumber}.{self.col - 1}'

    def addToken(self, tipo):
        self.tokens.append(CToken(self.palavraAuxiliar, tipo, self.calcularIndex1(), self.calcularIndex2()))

    def iniciar(self, line: str):
        self.col = 0
        self.s0(line)

    def s0(self, line: str):
        if self.col < len(line):
            if line[self.col].isnumeric():
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.col]
                self.col = self.col + 1
                self.s1(line)
            elif line[self.col] == "#":
                pass
            elif line[self.col] == "\"":
                self.col = self.col + 1
                self.s3(line)
            elif line[self.col].isalpha():
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.col]
                self.col = self.col + 1
                self.s4(line)
            else:
                self.col = self.col + 1
                self.s0(line)

    # INTEIRO
    def s1(self, line: str):
        if self.col < len(line):
            if line[self.col].isnumeric():
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.col]
                self.col = self.col + 1
                self.s1(line)
            elif line[self.col] == ".":
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.col]
                self.col = self.col + 1
                self.s2(line)
            elif line[self.col] == " " or line[self.col] == ";" or line[self.col] == ")":
                self.col = self.col + 1
                self.addToken(CToken.INT)
                self.palavraAuxiliar = ""
                self.s0(line)

    # FLOAT
    def s2(self, line: str):
        if self.col < len(line):
            if line[self.col].isnumeric():
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.col]
                self.col = self.col + 1
                self.s2(line)
            elif line[self.col] == " " or line[self.col] == ";" or line[self.col] == ")":
                self.col = self.col + 1
                self.addToken(CToken.FLOAT)
                self.palavraAuxiliar = ""
                self.s0(line)

    # STRING
    def s3(self, line: str):
        if self.col < len(line):
            if line[self.col] != "\"":
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.col]
                self.col = self.col + 1
                self.s3(line)
            elif line[self.col] == "\"":
                self.col = self.col + 1
                self.addToken(CToken.STRING)
                self.palavraAuxiliar = ""
                self.s0(line)

    # RESERVADA
    def s4(self, line: str):
        if self.col < len(line):
            if line[self.col].isalpha():
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.col]
                self.col = self.col + 1
                self.s4(line)
            elif line[self.col] in " ()=;+-/*%":
                if self.palavraAuxiliar in self.palavrasReservadas:
                    self.col = self.col + 1
                    self.addToken(CToken.KEYWORD)
                    self.palavraAuxiliar = ""
                    self.s0(line)
                else:
                    self.verificado = True
                    self.col = self.col + 1
                    self.s5(line)

    # IDENTIFICADOR
    def s5(self, line: str):
        if self.col <= len(line):
            if self.verificado:
                self.addToken(CToken.IDENTIFIER)
                self.palavraAuxiliar = ""
                self.verificado = False
                self.s0(line)

    def run(self):
        self.lineNumber = 1
        linhas = self.sentenca.split("\n")
        for line in linhas:
            line = list("".join(line))
            # print("Chamando iniciar para a linha ", line)
            self.iniciar(line)
            self.lineNumber += 1
