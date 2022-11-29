class CToken:
    STRING, INT, FLOAT, KEYWORD, IDENTIFIER, LPAR, RPAR, LCOL, RCOL, OARS, ATR, BOO, CAR, PTO, COM, NIN = range(16)

    TOKEN_NAMES = [
        "<STR>",
        "<NUMI>",
        "<NUMF>",
        "<PRS>",
        "<IDN>",
        "<LPAR>",
        "<RPAR>",
        "<LCOL>",
        "<RCOL>",
        "<OARS>",
        "<ATR>",
        "<BOO>",
        "<CAR>",
        "<PTO>",
        "<COM>",
        "<NIN>"
    ]

    TOKEN_COLORS = [
        "green1",
        "cyan",
        "cyan",
        "orange",
        "white",
        "red",
        "red",
        "yellow",
        "yellow",
        "white",
        "white",
        "DarkBlue",
        "orange",
        "white",
        "DarkGreen",
        "white"
    ]
    def __init__(self, texto, tipo, index1, index2):
        self.texto = texto
        self.tipo = tipo
        self.token = self.TOKEN_NAMES[tipo]
        self.index1 = index1
        self.index2 = index2

    def __str__(self) -> str:
        return f"Texto: {self.texto}, Token: {self.token}, inicio[Ln.Col]: {self.index1}, fim[Ln.Col]: {self.index2}"

    def __repr__(self) -> str:
        return self.__str__()