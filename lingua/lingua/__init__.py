"""LINGUA - AI-optimized programming language."""

from .lexer import Lexer, LexerError, Token
from .parser import parse, ParserError, LinguaProgram, ConceptNode, RelationNode, TransformNode, PatternNode
from .generator import generate_python, generate_json, generate_ir, CodeGenerator
from .reasoning import reason, ReasoningEngine, ConceptNotFoundError, ConceptExecutionError

__version__ = "1.0.0"
__all__ = [
    "Lexer",
    "LexerError", 
    "Token",
    "parse",
    "ParserError",
    "LinguaProgram",
    "ConceptNode",
    "RelationNode",
    "TransformNode",
    "PatternNode",
    "generate_python",
    "generate_json",
    "generate_ir",
    "CodeGenerator",
    "reason",
    "ReasoningEngine",
    "ConceptNotFoundError",
    "ConceptExecutionError",
]