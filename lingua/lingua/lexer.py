"""LINGUA Lexer - Tokenizer for LINGUA programming language."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class TokenType(Enum):
    DELIMITER_OPEN = auto()
    DELIMITER_CLOSE = auto()
    BLOCK_OPEN = auto()
    BLOCK_CLOSE = auto()
    SEPARATOR = auto()
    COMMENT = auto()
    CONCEPT_KW = auto()
    RELATION_KW = auto()
    TRANSFORM_KW = auto()
    PATTERN_KW = auto()
    TYPE_KW = auto()
    INPUT_KW = auto()
    OUTPUT_KW = auto()
    REASON_KW = auto()
    IMPL_KW = auto()
    FROM_KW = auto()
    TO_KW = auto()
    CAUSE_KW = auto()
    EFFECT_KW = auto()
    PRESERVE_KW = auto()
    CONSTRAINT_KW = auto()
    MAP_KW = auto()
    EVIDENCE_KW = auto()
    CONTEXT_KW = auto()
    RESOLVE_KW = auto()
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COLON = auto()
    COMMA = auto()
    NEWLINE = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LPAREN = auto()
    RPAREN = auto()
    DOT = auto()
    EQ = auto()
    LT = auto()
    GT = auto()
    EOF = auto()


KEYWORDS = {
    'CONCEPT': TokenType.CONCEPT_KW,
    'RELATION': TokenType.RELATION_KW,
    'TRANSFORM': TokenType.TRANSFORM_KW,
    'PATTERN': TokenType.PATTERN_KW,
    'TYPE': TokenType.TYPE_KW,
    'INPUT': TokenType.INPUT_KW,
    'OUTPUT': TokenType.OUTPUT_KW,
    'REASON': TokenType.REASON_KW,
    'IMPL': TokenType.IMPL_KW,
    'FROM': TokenType.FROM_KW,
    'TO': TokenType.TO_KW,
    'CAUSE': TokenType.CAUSE_KW,
    'EFFECT': TokenType.EFFECT_KW,
    'PRESERVE': TokenType.PRESERVE_KW,
    'CONSTRAINT': TokenType.CONSTRAINT_KW,
    'MAP': TokenType.MAP_KW,
    'EVIDENCE': TokenType.EVIDENCE_KW,
    'CONTEXT': TokenType.CONTEXT_KW,
    'RESOLVE': TokenType.RESOLVE_KW,
}


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer error at line {line}, column {column}: {message}")


class Lexer:
    DELIMITER_OPEN = '§'
    DELIMITER_CLOSE = '§'
    BLOCK_OPEN = '╔═══╗'
    BLOCK_CLOSE = '╚═══╝'
    SEPARATOR = '│'
    COMMENT = '◇'

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self._delimiter_count = 0

    def tokenize(self) -> list[Token]:
        while self.pos < len(self.source):
            self._skip_whitespace()
            if self.pos >= len(self.source):
                break

            char = self.source[self.pos]

            if char == '\n':
                self._add_token(TokenType.NEWLINE, '\n')
                self.line += 1
                self.column = 1
                self.pos += 1
                continue

            if self._match_string('╔═══╗'):
                self._add_token(TokenType.BLOCK_OPEN, '╔═══╗')
                self.pos += 5
                self.column += 5
                continue

            if self._match_string('╚═══╝'):
                self._add_token(TokenType.BLOCK_CLOSE, '╚═══╝')
                self.pos += 5
                self.column += 5
                continue

            if self.source[self.pos:].startswith('§'):
                if self._delimiter_count % 2 == 0:
                    self._add_token(TokenType.DELIMITER_OPEN, '§')
                else:
                    self._add_token(TokenType.DELIMITER_CLOSE, '§')
                self._delimiter_count += 1
                self.pos += 1
                self.column += 1
                continue

            if self.source[self.pos:].startswith('│'):
                self._add_token(TokenType.SEPARATOR, '│')
                self.pos += 1
                self.column += 1
                continue

            if self.source[self.pos:].startswith('◇'):
                self._skip_comment()
                continue

            if char == '"':
                self._read_string()
                continue

            if char.isdigit():
                self._read_number()
                continue

            if char.isalpha() or char == '_':
                self._read_identifier()
                continue

            if char == '[':
                self._add_token(TokenType.LBRACKET, '[')
                self.pos += 1
                self.column += 1
                continue

            if char == ']':
                self._add_token(TokenType.RBRACKET, ']')
                self.pos += 1
                self.column += 1
                continue

            if char == '{':
                self._add_token(TokenType.LBRACE, '{')
                self.pos += 1
                self.column += 1
                continue

            if char == '}':
                self._add_token(TokenType.RBRACE, '}')
                self.pos += 1
                self.column += 1
                continue

            if char == ':':
                self._add_token(TokenType.COLON, ':')
                self.pos += 1
                self.column += 1
                continue

            if char == ',':
                self._add_token(TokenType.COMMA, ',')
                self.pos += 1
                self.column += 1
                continue

            if char == '+':
                self._add_token(TokenType.PLUS, '+')
                self.pos += 1
                self.column += 1
                continue

            if char == '-':
                self._add_token(TokenType.MINUS, '-')
                self.pos += 1
                self.column += 1
                continue

            if char == '*':
                self._add_token(TokenType.STAR, '*')
                self.pos += 1
                self.column += 1
                continue

            if char == '/':
                self._add_token(TokenType.SLASH, '/')
                self.pos += 1
                self.column += 1
                continue

            if char == '(':
                self._add_token(TokenType.LPAREN, '(')
                self.pos += 1
                self.column += 1
                continue

            if char == ')':
                self._add_token(TokenType.RPAREN, ')')
                self.pos += 1
                self.column += 1
                continue

            if char == '.':
                self._add_token(TokenType.DOT, '.')
                self.pos += 1
                self.column += 1
                continue

            if char == '=':
                self._add_token(TokenType.EQ, '=')
                self.pos += 1
                self.column += 1
                continue

            if char == '<':
                self._add_token(TokenType.LT, '<')
                self.pos += 1
                self.column += 1
                continue

            if char == '>':
                self._add_token(TokenType.GT, '>')
                self.pos += 1
                self.column += 1
                continue

            if ord(char) > 127:
                self._add_token(TokenType.IDENTIFIER, char)
                self.pos += 1
                self.column += 1
                continue

            raise LexerError(f"Unexpected character: {char!r}", self.line, self.column)

        self._add_token(TokenType.EOF, '')
        return self.tokens

    def _skip_whitespace(self):
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char in ' \t\r':
                self.pos += 1
                self.column += 1
            else:
                break

    def _skip_comment(self):
        start_col = self.column
        self.pos += 1
        self.column += 1
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self.pos += 1
            self.column += 1
        comment_text = self.source[start:self.pos]
        self._add_token(TokenType.COMMENT, comment_text)

    def _match_string(self, s: str) -> bool:
        return self.source[self.pos:].startswith(s)

    def _read_string(self):
        start_col = self.column
        self.pos += 1
        self.column += 1
        start = self.pos
        value = ''
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == '\\' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '"':
                value += self.source[self.pos + 1]
                self.pos += 2
                self.column += 2
                continue
            if self.source[self.pos] == '\n':
                raise LexerError("Unterminated string", self.line, start_col)
            value += self.source[self.pos]
            self.pos += 1
            self.column += 1
        if self.pos >= len(self.source):
            raise LexerError("Unterminated string", self.line, start_col)
        self._add_token(TokenType.STRING, value)
        self.pos += 1
        self.column += 1

    def _read_number(self):
        start_col = self.column
        start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            self.pos += 1
            self.column += 1
        value = self.source[start:self.pos]
        self._add_token(TokenType.NUMBER, value)

    def _read_identifier(self):
        start_col = self.column
        start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self.pos += 1
            self.column += 1
        value = self.source[start:self.pos]
        token_type = KEYWORDS.get(value, TokenType.IDENTIFIER)
        self._add_token(token_type, value)

    def _add_token(self, token_type: TokenType, value: str):
        self.tokens.append(Token(token_type, value, self.line, self.column))