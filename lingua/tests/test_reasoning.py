"""Tests for LINGUA reasoning engine."""

import pytest
from lingua.parser import parse
from lingua.reasoning import (
    ReasoningEngine, ConceptNotFoundError, ConceptExecutionError
)


def test_execute_string_literal():
    source = '''§
╔═══╗ CONCEPT saluto
│ TYPE operazione
│ INPUT []
│ OUTPUT stringa
│ REASON "Genera un saluto"
│ IMPL "Ciao, mondo!"
╚═══╝
§'''
    program = parse(source)
    engine = ReasoningEngine(program)
    result = engine.execute_concept("saluto")
    assert result == "Ciao, mondo!"


def test_execute_number_literal():
    source = '''§
╔═══╗ CONCEPT numero
│ TYPE dato
│ OUTPUT numero
│ REASON "Un numero"
│ IMPL "42"
╚═══╝
§'''
    program = parse(source)
    engine = ReasoningEngine(program)
    result = engine.execute_concept("numero")
    assert result == "42"


def test_execute_with_params():
    source = '''§
╔═══╗ CONCEPT saluta
│ TYPE operazione
│ INPUT [nome: stringa]
│ OUTPUT stringa
│ REASON "Saluta qualcuno"
│ IMPL "Ciao, {nome}!"
╚═══╝
§'''
    program = parse(source)
    engine = ReasoningEngine(program)
    result = engine.execute_concept("saluta", nome="Mario")
    assert result == "Ciao, Mario!"


def test_execute_missing_input():
    source = '''§
╔═══╗ CONCEPT saluta
│ TYPE operazione
│ INPUT [nome: stringa]
│ OUTPUT stringa
│ REASON "Saluta qualcuno"
│ IMPL "Ciao, {nome}!"
╚═══╝
§'''
    program = parse(source)
    engine = ReasoningEngine(program)
    with pytest.raises(ConceptExecutionError) as exc_info:
        engine.execute_concept("saluta")
    assert "Missing required input: nome" in str(exc_info.value)


def test_execute_concept_not_found():
    source = '''§
╔═══╗ CONCEPT esiste
│ TYPE dato
│ OUTPUT stringa
│ REASON "Esiste"
│ IMPL "si"
╚═══╝
§'''
    program = parse(source)
    engine = ReasoningEngine(program)
    with pytest.raises(ConceptNotFoundError):
        engine.execute_concept("non_esiste")


def test_execute_python_expr():
    source = '''§
╔═══╗ CONCEPT somma
│ TYPE operazione
│ INPUT [a: numero, b: numero]
│ OUTPUT numero
│ REASON "Somma due numeri"
│ IMPL "a + b"
╚═══╝
§'''
    program = parse(source)
    engine = ReasoningEngine(program)
    result = engine.execute_concept("somma", a=3, b=5)
    assert result == 8


def test_reason_finds_concept_by_name():
    source = '''§
╔═══╗ CONCEPT saluto
│ TYPE operazione
│ INPUT []
│ OUTPUT stringa
│ REASON "Genera un saluto"
│ IMPL "Ciao!"
╚═══╝
§'''
    program = parse(source)
    engine = ReasoningEngine(program)
    result = engine.reason("saluto")
    assert "saluto" in result["concepts_used"]
    assert result["result"] == "Ciao!"


def test_reason_with_context():
    source = '''§
╔═══╗ CONCEPT saluto
│ TYPE operazione
│ INPUT [nome: stringa]
│ OUTPUT stringa
│ REASON "Genera un saluto personalizzato"
│ IMPL "Ciao, {nome}!"
╚═══╝
§'''
    program = parse(source)
    engine = ReasoningEngine(program)
    result = engine.reason("saluto", context={"nome": "Luca"})
    assert "saluto" in result["concepts_used"]
    assert result["result"] == "Ciao, Luca!"