"""LINGUA Code Generator - Generates Python, JSON, and IR output."""

import json
from dataclasses import dataclass, asdict
from .parser import (
    LinguaProgram, ConceptNode, RelationNode,
    TransformNode, PatternNode
)


class CodeGenerator:
    def __init__(self, program: LinguaProgram):
        self.program = program

    def to_python(self) -> str:
        lines = ["# GENERATED FROM LINGUA", ""]

        for concept in self.program.concepts:
            lines.append(self._generate_concept_function(concept))

        for transform in self.program.transforms:
            lines.append(self._generate_transform_function(transform))

        return "\n".join(lines)

    def _generate_concept_function(self, concept: ConceptNode) -> str:
        lines = []
        params = [f"{name}: {type_name}" for name, type_name in concept.input_types]
        params_str = ", ".join(params) if params else ""

        lines.append(f"def {concept.name}({params_str}):")
        lines.append(f'    """{concept.reason}"""')

        if concept.concept_type == "operazione":
            lines.append(f"    return {concept.impl!r}")
        elif concept.concept_type == "effetto":
            lines.append(f"    {concept.impl!r}")
        elif concept.concept_type == "dato":
            lines.append(f"    return {concept.impl!r}")
        elif concept.concept_type == "stato":
            lines.append(f"    return {concept.impl!r}")

        lines.append("")
        return "\n".join(lines)

    def _generate_transform_function(self, transform: TransformNode) -> str:
        lines = []
        params = ", ".join(transform.cause)
        lines.append(f"def {transform.name}({params}):")
        lines.append(f'    """TRANSFORM: {transform.constraint}"""')
        lines.append(f"    # MAP: {transform.map}")
        lines.append(f"    pass")
        lines.append("")
        return "\n".join(lines)

    def to_json(self) -> str:
        data = {
            "lingua_version": "1.0.0",
            "concepts": [
                {
                    "name": c.name,
                    "type": c.concept_type,
                    "input_types": [{"name": n, "type": t} for n, t in c.input_types],
                    "output_type": c.output_type,
                    "reason": c.reason,
                    "impl": c.impl,
                }
                for c in self.program.concepts
            ],
            "relations": [
                {
                    "name": r.name,
                    "from": r.from_concept,
                    "to": r.to_concept,
                    "type": r.relation_type,
                    "reason": r.reason,
                }
                for r in self.program.relations
            ],
            "transforms": [
                {
                    "name": t.name,
                    "cause": t.cause,
                    "effect": t.effect,
                    "preserve": t.preserve,
                    "constraint": t.constraint,
                    "map": t.map,
                }
                for t in self.program.transforms
            ],
            "patterns": [
                {
                    "name": p.name,
                    "evidence": p.evidence,
                    "context": p.context,
                    "resolve": p.resolve,
                }
                for p in self.program.patterns
            ],
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    def to_ir(self) -> dict:
        ir = {
            "version": "1.0.0",
            "concepts": {},
            "relations": [],
            "transforms": {},
            "patterns": {},
        }

        for concept in self.program.concepts:
            ir["concepts"][concept.name] = {
                "kind": "CONCEPT",
                "type": concept.concept_type,
                "input": concept.input_types,
                "output": concept.output_type,
                "reason": concept.reason,
                "impl": concept.impl,
            }

        for relation in self.program.relations:
            ir["relations"].append({
                "from": relation.from_concept,
                "to": relation.to_concept,
                "type": relation.relation_type,
            })

        for transform in self.program.transforms:
            ir["transforms"][transform.name] = {
                "kind": "TRANSFORM",
                "cause": transform.cause,
                "effect": transform.effect,
                "preserve": transform.preserve,
                "constraint": transform.constraint,
            }

        for pattern in self.program.patterns:
            ir["patterns"][pattern.name] = {
                "kind": "PATTERN",
                "evidence": pattern.evidence,
                "context": pattern.context,
                "resolve": pattern.resolve,
            }

        return ir


def generate_python(program: LinguaProgram) -> str:
    return CodeGenerator(program).to_python()


def generate_json(program: LinguaProgram) -> str:
    return CodeGenerator(program).to_json()


def generate_ir(program: LinguaProgram) -> dict:
    return CodeGenerator(program).to_ir()