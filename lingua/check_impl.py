from lingua.parser import parse
from lingua.reasoning import ReasoningEngine

# Test 1: Python expression without outer quotes
source = """§
CONCEPT somma
TYPE operazione
INPUT [a: numero, b: numero]
OUTPUT numero
REASON "Somma due numeri"
IMPL a + b
§"""
program = parse(source)
for c in program.concepts:
    print(f"name: {c.name}, impl: {repr(c.impl)}")
engine = ReasoningEngine(program)
result = engine.execute_concept("somma", a=3, b=5)
print(f"execute_concept result: {repr(result)}")