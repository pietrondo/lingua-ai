"""LINGUA Parser - AST builder for LINGUA programming language."""

from dataclasses import dataclass, field
from typing import Optional
from .lexer import Token, TokenType, Lexer


@dataclass
class ConceptNode:
    name: str
    concept_type: str
    input_types: list[tuple[str, str]]
    output_type: str
    reason: str
    impl: str
    fields: Optional[list[tuple[str, str]]] = None


@dataclass
class RelationNode:
    name: str
    from_concept: str
    to_concept: str
    relation_type: str
    reason: str


@dataclass
class TransformNode:
    name: str
    cause: list[str]
    effect: str
    preserve: list[str]
    constraint: str
    map: str


@dataclass
class PatternNode:
    name: str
    evidence: str
    context: list[str]
    resolve: str


@dataclass
class LinguaProgram:
    concepts: list[ConceptNode] = field(default_factory=list)
    relations: list[RelationNode] = field(default_factory=list)
    transforms: list[TransformNode] = field(default_factory=list)
    patterns: list[PatternNode] = field(default_factory=list)


class ParserError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Parser error at line {line}, column {column}: {message}")


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> LinguaProgram:
        program = LinguaProgram()
        while not self._is_at_end():
            if self._check(TokenType.DELIMITER_OPEN):
                self._parse_block_content(program)
                if self._check(TokenType.DELIMITER_CLOSE):
                    self._advance()
            elif self._check(TokenType.BLOCK_OPEN):
                node = self._parse_block()
                if node:
                    if isinstance(node, ConceptNode):
                        program.concepts.append(node)
                    elif isinstance(node, RelationNode):
                        program.relations.append(node)
                    elif isinstance(node, TransformNode):
                        program.transforms.append(node)
                    elif isinstance(node, PatternNode):
                        program.patterns.append(node)
            else:
                self._advance()
        return program

    def _peek_next(self) -> Token:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return self.tokens[self.pos]

    def _parse_block_content(self, program: LinguaProgram):
        while not self._check(TokenType.DELIMITER_CLOSE) and not self._is_at_end():
            if self._check(TokenType.DELIMITER_OPEN):
                self._advance()
                self._consume_newlines()
            if self._check(TokenType.BLOCK_OPEN):
                self._advance()
                self._consume_newlines()
                keyword = self._expect_one_of(TokenType.CONCEPT_KW, TokenType.RELATION_KW, TokenType.TRANSFORM_KW, TokenType.PATTERN_KW)
                name = self._expect(TokenType.IDENTIFIER).value
                self._consume_newlines()
                if keyword.type == TokenType.CONCEPT_KW:
                    node = self._parse_concept(name)
                elif keyword.type == TokenType.RELATION_KW:
                    node = self._parse_relation(name)
                elif keyword.type == TokenType.TRANSFORM_KW:
                    node = self._parse_transform(name)
                elif keyword.type == TokenType.PATTERN_KW:
                    node = self._parse_pattern(name)
                if node:
                    if isinstance(node, ConceptNode):
                        program.concepts.append(node)
                    elif isinstance(node, RelationNode):
                        program.relations.append(node)
                    elif isinstance(node, TransformNode):
                        program.transforms.append(node)
                    elif isinstance(node, PatternNode):
                        program.patterns.append(node)
            elif self._check(TokenType.BLOCK_CLOSE):
                self._advance()
                self._consume_newlines()
            else:
                self._advance()
        return program

    def _parse_block(self):
        if self._check(TokenType.BLOCK_OPEN):
            self._advance()
        elif self._check(TokenType.DELIMITER_OPEN):
            self._advance()
        self._consume_newlines()
        keyword = self._expect_one_of(TokenType.CONCEPT_KW, TokenType.RELATION_KW, TokenType.TRANSFORM_KW, TokenType.PATTERN_KW)
        name = self._expect(TokenType.IDENTIFIER).value
        self._consume_newlines()

        if keyword.type == TokenType.CONCEPT_KW:
            node = self._parse_concept(name)
        elif keyword.type == TokenType.RELATION_KW:
            node = self._parse_relation(name)
        elif keyword.type == TokenType.TRANSFORM_KW:
            node = self._parse_transform(name)
        elif keyword.type == TokenType.PATTERN_KW:
            node = self._parse_pattern(name)

        return node

    def _parse_concept(self, name: str) -> ConceptNode:
        fields = []
        concept_type = ""
        input_types = []
        output_type = ""
        reason = ""
        impl = ""

        while not self._check(TokenType.BLOCK_CLOSE) and not self._check(TokenType.DELIMITER_CLOSE) and not self._is_at_end():
            kw = self._current().type
            self._consume_newlines()

            if kw == TokenType.TYPE_KW:
                self._expect(TokenType.TYPE_KW)
                concept_type = self._expect(TokenType.IDENTIFIER).value
            elif kw == TokenType.INPUT_KW:
                self._expect(TokenType.INPUT_KW)
                input_types = self._parse_field_list()
            elif kw == TokenType.OUTPUT_KW:
                self._expect(TokenType.OUTPUT_KW)
                output_type = self._expect(TokenType.IDENTIFIER).value
            elif kw == TokenType.REASON_KW:
                self._expect(TokenType.REASON_KW)
                reason = self._parse_string_or_identifier()
            elif kw == TokenType.IMPL_KW:
                self._expect(TokenType.IMPL_KW)
                impl = self._parse_impl()
            elif kw == TokenType.CAMPI_KW if hasattr(TokenType, 'CAMPI_KW') else False:
                self._expect(TokenType.CAMPI_KW)
                fields = self._parse_field_list()
            else:
                self._advance()

            self._consume_newlines()

        self._expect_one_of(TokenType.BLOCK_CLOSE, TokenType.DELIMITER_CLOSE)
        return ConceptNode(name, concept_type, input_types, output_type, reason, impl, fields if fields else None)

    def _parse_relation(self, name: str) -> RelationNode:
        from_concept = ""
        to_concept = ""
        relation_type = ""
        reason = ""

        while not self._check(TokenType.BLOCK_CLOSE) and not self._check(TokenType.DELIMITER_CLOSE) and not self._is_at_end():
            kw = self._current().type
            self._consume_newlines()

            if kw == TokenType.FROM_KW:
                self._expect(TokenType.FROM_KW)
                from_concept = self._expect(TokenType.IDENTIFIER).value
            elif kw == TokenType.TO_KW:
                self._expect(TokenType.TO_KW)
                to_concept = self._expect(TokenType.IDENTIFIER).value
            elif kw == TokenType.TYPE_KW:
                self._expect(TokenType.TYPE_KW)
                relation_type = self._expect(TokenType.IDENTIFIER).value
            elif kw == TokenType.REASON_KW:
                self._expect(TokenType.REASON_KW)
                reason = self._parse_string_or_identifier()
            else:
                self._advance()

            self._consume_newlines()

        self._expect_one_of(TokenType.BLOCK_CLOSE, TokenType.DELIMITER_CLOSE)
        return RelationNode(name, from_concept, to_concept, relation_type, reason)

    def _parse_transform(self, name: str) -> TransformNode:
        cause = []
        effect = ""
        preserve = []
        constraint = ""
        map_str = ""

        while not self._check(TokenType.BLOCK_CLOSE) and not self._check(TokenType.DELIMITER_CLOSE) and not self._is_at_end():
            kw = self._current().type
            self._consume_newlines()

            if kw == TokenType.CAUSE_KW:
                self._expect(TokenType.CAUSE_KW)
                cause = self._parse_list()
            elif kw == TokenType.EFFECT_KW:
                self._expect(TokenType.EFFECT_KW)
                effect = self._parse_string_or_identifier()
            elif kw == TokenType.PRESERVE_KW:
                self._expect(TokenType.PRESERVE_KW)
                preserve = self._parse_list()
            elif kw == TokenType.CONSTRAINT_KW:
                self._expect(TokenType.CONSTRAINT_KW)
                constraint = self._parse_string_or_identifier()
            elif kw == TokenType.MAP_KW:
                self._expect(TokenType.MAP_KW)
                map_str = self._parse_string_or_identifier()
            else:
                self._advance()

            self._consume_newlines()

        self._expect_one_of(TokenType.BLOCK_CLOSE, TokenType.DELIMITER_CLOSE)
        return TransformNode(name, cause, effect, preserve, constraint, map_str)

    def _parse_pattern(self, name: str) -> PatternNode:
        evidence = ""
        context = []
        resolve = ""

        while not self._check(TokenType.BLOCK_CLOSE) and not self._check(TokenType.DELIMITER_CLOSE) and not self._is_at_end():
            kw = self._current().type
            self._consume_newlines()

            if kw == TokenType.EVIDENCE_KW:
                self._expect(TokenType.EVIDENCE_KW)
                evidence = self._parse_string_or_identifier()
            elif kw == TokenType.CONTEXT_KW:
                self._expect(TokenType.CONTEXT_KW)
                context = self._parse_list()
            elif kw == TokenType.RESOLVE_KW:
                self._expect(TokenType.RESOLVE_KW)
                resolve = self._parse_string_or_identifier()
            else:
                self._advance()

            self._consume_newlines()

        self._expect_one_of(TokenType.BLOCK_CLOSE, TokenType.DELIMITER_CLOSE)
        return PatternNode(name, evidence, context, resolve)

    def _parse_field_list(self) -> list[tuple[str, str]]:
        result = []
        self._expect(TokenType.LBRACKET)
        while not self._check(TokenType.RBRACKET) and not self._is_at_end():
            name = self._expect(TokenType.IDENTIFIER).value
            self._expect(TokenType.COLON if hasattr(TokenType, 'COLON') else TokenType.IDENTIFIER)
            type_name = self._expect(TokenType.IDENTIFIER).value
            result.append((name, type_name))
            if self._check(TokenType.COMMA if hasattr(TokenType, 'COMMA') else TokenType.IDENTIFIER):
                self._advance()
        self._expect(TokenType.RBRACKET)
        return result

    def _parse_list(self) -> list[str]:
        result = []
        self._expect(TokenType.LBRACKET)
        while not self._check(TokenType.RBRACKET) and not self._is_at_end():
            if self._check(TokenType.STRING) or self._check(TokenType.IDENTIFIER):
                result.append(self._advance().value)
            else:
                self._advance()
            if self._check(TokenType.COMMA if hasattr(TokenType, 'COMMA') else TokenType.IDENTIFIER):
                self._advance()
        self._expect(TokenType.RBRACKET)
        return result

    def _parse_string_or_identifier(self) -> str:
        if self._check(TokenType.STRING):
            return self._advance().value
        return self._expect(TokenType.IDENTIFIER).value

    def _parse_impl(self) -> str:
        parts = []
        while not self._check(TokenType.BLOCK_CLOSE) and not self._check(TokenType.NEWLINE) and not self._check(TokenType.SEPARATOR) and not self._is_at_end():
            token = self._advance()
            if token.type == TokenType.STRING:
                parts.append(f'"{token.value}"')
                break
            if token.type in (TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.PLUS, TokenType.MINUS,
                              TokenType.STAR, TokenType.SLASH, TokenType.LPAREN, TokenType.RPAREN,
                              TokenType.COMMA, TokenType.DOT, TokenType.EQ, TokenType.LT, TokenType.GT):
                parts.append(token.value)
                continue
            if self._is_at_end():
                break
        return " ".join(parts)

    def _consume_newlines(self):
        while self._check(TokenType.NEWLINE):
            self._advance()

    def _check(self, *types: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._current().type in types

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.pos += 1
        return self.tokens[self.pos - 1]

    def _current(self) -> Token:
        return self.tokens[self.pos]

    def _is_at_end(self) -> bool:
        return self._current().type == TokenType.EOF

    def _expect(self, token_type: TokenType) -> Token:
        if self._check(token_type):
            return self._advance()
        raise ParserError(f"Expected {token_type}, got {self._current().type}", self._current().line, self._current().column)

    def _expect_one_of(self, *types: TokenType) -> Token:
        if self._check(*types):
            return self._advance()
        raise ParserError(f"Expected one of {types}, got {self._current().type}", self._current().line, self._current().column)


def parse(source: str) -> LinguaProgram:
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()