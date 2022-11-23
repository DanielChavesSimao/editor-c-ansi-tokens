class LuguimoAFD:

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
        self.cont = 0
        self.sentenca = sentenca
        self.inteiro = 0
        self.inteiroLista = []
        self.decimal = 0
        self.decimalLista = []
        self._string = 0
        self._stringLista = []
        self.reservada = 0
        self.reservadaLista = []
        self.identificador = 0
        self.identificadorLista = []
        self.palavraAuxiliar = ""
        self.verificado = False
        self.palavrasReservadas = [
            "auto", "break", "case", "char", "const", "self.continue",
            "default", "do", "double", "else", "enum", "extern",
            "float", "for", "goto", "if", "inline", "int", "long",
            "register", "restrict", "return", "short", "while",
            "signed", "static", "struct", "switch", "typedef",
            "union", "void", "volatile", "while"
        ]

    def iniciar(self, line: str):
        self.cont = 0
        self.s0(line)

    def s0(self, line: str):
        if self.cont < len(line):
            if line[self.cont].isnumeric():
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.cont]
                self.cont = self.cont + 1
                self.s2(line)
            elif line[self.cont] == "#":
                pass
            elif line[self.cont] == "\"":
                self.cont = self.cont + 1
                self.s4(line)
            elif line[self.cont].isalpha():
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.cont]
                self.cont = self.cont + 1
                self.s5(line)
            else:
                self.cont = self.cont + 1
                self.s0(line)

    # INTEIRO
    def s2(self, line: str):
        if self.cont < len(line):
            if line[self.cont].isnumeric():
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.cont]
                self.cont = self.cont + 1
                self.s2(line)
            elif line[self.cont] == ".":
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.cont]
                self.cont = self.cont + 1
                self.s3(line)
            elif line[self.cont] == " " or line[self.cont] == ";" or line[self.cont] == ")":
                self.cont = self.cont + 1
                self.inteiro = self.inteiro + 1
                self.inteiroLista.append(self.palavraAuxiliar)
                self.palavraAuxiliar = ""
                self.s0(line)

    # FLOAT
    def s3(self, line: str):
        if self.cont < len(line):
            if line[self.cont].isnumeric():
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.cont]
                self.cont = self.cont + 1
                self.s3(line)
            elif line[self.cont] == " " or line[self.cont] == ";" or line[self.cont] == ")":
                self.cont = self.cont + 1
                self.decimal = self.decimal + 1
                self.decimalLista.append(self.palavraAuxiliar)
                self.palavraAuxiliar = ""
                self.s0(line)

    # STRING
    def s4(self, line: str):
        if self.cont < len(line):
            if line[self.cont] != "\"":
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.cont]
                self.cont = self.cont + 1
                self.s4(line)
            elif line[self.cont] == "\"":
                self.cont = self.cont + 1
                self._string = self._string + 1
                self._stringLista.append(self.palavraAuxiliar)
                self.palavraAuxiliar = ""
                self.s0(line)

    # RESERVADA
    def s5(self, line: str):
        if self.cont < len(line):
            if line[self.cont].isalpha():
                self.palavraAuxiliar = self.palavraAuxiliar + line[self.cont]
                self.cont = self.cont + 1
                self.s5(line)
            elif line[self.cont] in " ()=;+-/*%":
                if self.palavraAuxiliar in self.palavrasReservadas:
                    self.reservada = self.reservada + 1
                    self.reservadaLista.append(self.palavraAuxiliar)
                    self.palavraAuxiliar = ""
                    self.cont = self.cont + 1
                    self.s0(line)
                else:
                    self.verificado = True
                    self.cont = self.cont + 1
                    self.s6(line)

    # IDENTIFICADOR
    def s6(self, line: str):
        if self.cont <= len(line):
            if self.verificado:
                self.identificador = self.identificador + 1
                self.identificadorLista.append(self.palavraAuxiliar)
                self.palavraAuxiliar = ""
                self.verificado = False
                self.s0(line)

    def run(self):
        linhas = self.sentenca.split("\n")
        for line in linhas:
            line = list("".join(line))
            # print("Chamando iniciar para a linha ", line)
            self.iniciar(line)

    def __str__(self):
        return "\n".join([
            f"Reservada = {self.reservada}",
            f"  {self.reservadaLista}",
            f"Inteiros = {self.inteiro}",
            f"  {self.inteiroLista}",
            f"Identificador = {self.identificador}",
            f"  {self.identificadorLista}",
            f"Decimais = {self.decimal}",
            f"  {self.decimalLista}",
            f"Strings = {self._string}",
            f"  {self._stringLista}",
        ])
