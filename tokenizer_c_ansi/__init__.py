# adapted from python re docs example

from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    line_start: int
    line_end: int
    column_start: int
    column_end: int


def tokenize(code):
    keywords = {
        "auto", "break", "case", "char", "const", "continue",
        "default", "do", "double", "else", "enum", "extern",
        "float", "for", "goto", "if", "inline", "int", "long",
        "register", "restrict", "return", "short", "while",
        "signed", "static", "struct", "switch", "typedef",
        "union", "void", "volatile", "while"
    }
    keywords_regex = '|'.join(keywords) 
    token_specification = [
        ('KEYWORD', keywords_regex),
        ('NUMBER', r'\d+(\.\d*)?'),  # Integer or decimal number
        ('CHAR', r"'.'"),  # Character
        ('STRING', r'".*"'),  # String
        ('BOO', r'true|false'),  # Logical constants
        ('LPAR', r'\('),  # Left parentheses
        ('RPAR', r'\)'),  # Right parentheses
        ('LCO', r'\['),  # Left square bracket
        ('RCO', r'\]'),  # Right square bracket
        ('LCUR', r'\{'),  # Left curly bracket
        ('RCUR', r'\}'),  # Right curly bracket
        ('COMMA', r','),  # Comma
        # ('HASH', r'#'),  # pre-processor
        ('ASTERISK', r'\*'),  # pointer
        # ('TILDE', r'~'), # destructor
        # ('PERIOD', r'\.') # member accessor
        ('COMMENT', r'//'),  # comentário
        ('ASSIGN', r'='),  # Assignment operator
        ('END', r';'),  # Statement terminator
        ('ID', r'([A-Za-z_][\w_]*){1,31}'),  # Identifiers
        # Arithmetic, logic and relational operators
        ('OP', r'[+\-*/%]|[<>=!]=|&&|\|\|'),
        ('NEWLINE',  r'\n'),  # Line endings
        ('SKIP',     r'[ \t]+|#.+'),  # Skip over spaces and tabs and preprocessor
        ('MISMATCH', r'.'),  # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            yield Token(kind, value, line_num - 1, line_num - 1, column, column + 1)
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        # TODO multiline
        yield Token(kind, value, line_num, line_num, column, column + mo.end() - mo.start())
