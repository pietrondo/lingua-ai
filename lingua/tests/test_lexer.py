"""Tests for LINGUA lexer."""

import pytest
from lingua.lexer import Lexer, LexerError, TokenType


def test_lexer_delimiters():
    source = "§\n§"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.DELIMITER_OPEN
    assert tokens[1].type == TokenType.NEWLINE
    assert tokens[2].type == TokenType.DELIMITER_CLOSE


def test_lexer_block_delimiters():
    source = "╔═══╗ test ╚═══╝"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.BLOCK_OPEN
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[2].type == TokenType.BLOCK_CLOSE


def test_lexer_separator():
    source = "│"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.SEPARATOR


def test_lexer_comment():
    source = "◇ This is a comment"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.COMMENT


def test_lexer_keywords():
    source = "CONCEPT RELATION TRANSFORM PATTERN"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.CONCEPT_KW
    assert tokens[1].type == TokenType.RELATION_KW
    assert tokens[2].type == TokenType.TRANSFORM_KW
    assert tokens[3].type == TokenType.PATTERN_KW


def test_lexer_string():
    source = '"hello world"'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "hello world"


def test_lexer_number():
    source = "42 3.14"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == "42"
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].value == "3.14"


def test_lexer_identifier():
    source = "my_function variable123"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "my_function"
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == "variable123"


def test_lexer_error():
    source = "@ invalid"
    lexer = Lexer(source)
    with pytest.raises(LexerError):
        lexer.tokenize()