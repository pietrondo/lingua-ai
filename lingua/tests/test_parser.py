"""Tests for LINGUA parser."""

import pytest
from lingua.parser import parse, ParserError


def test_parse_simple_concept():
    source = '''§
╔═══╗ CONCEPT saluto
│ TYPE operazione
│ INPUT []
│ OUTPUT stringa
│ REASON "Genera un messaggio di saluto"
│ IMPL "Ciao, mondo!"
╚═══╝
§'''
    program = parse(source)
    assert len(program.concepts) == 1
    assert program.concepts[0].name == "saluto"
    assert program.concepts[0].concept_type == "operazione"
    assert program.concepts[0].output_type == "stringa"


def test_parse_empty_program():
    source = ""
    program = parse(source)
    assert len(program.concepts) == 0
    assert len(program.relations) == 0


def test_parse_multiple_concepts():
    source = '''§
╔═══╗ CONCEPT concetto1
│ TYPE dato
│ OUTPUT numero
│ REASON "Un numero"
│ IMPL "42"
╚═══╝

╔═══╗ CONCEPT concetto2
│ TYPE operazione
│ INPUT []
│ OUTPUT numero
│ REASON "Un altro numero"
│ IMPL "100"
╚═══╝
§'''
    program = parse(source)
    assert len(program.concepts) == 2