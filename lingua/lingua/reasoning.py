"""LINGUA Reasoning Engine - Executes LINGUA programs."""

from dataclasses import dataclass, field
from typing import Any, Optional
from .parser import LinguaProgram, ConceptNode, RelationNode, TransformNode, PatternNode


@dataclass
class ConceptNotFoundError(Exception):
    name: str
    def __str__(self) -> str:
        return f"Concept not found: {self.name}"


@dataclass
class ConceptExecutionError(Exception):
    concept: str
    cause: str
    def __str__(self) -> str:
        return f"Error executing concept '{self.concept}': {self.cause}"


@dataclass
class ReasoningEngine:
    program: LinguaProgram
    concept_graph: dict[str, ConceptNode] = field(default_factory=dict)
    concept_instances: dict[str, Any] = field(default_factory=dict)
    transform_results: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self._build_concept_graph()
        self._build_transform_index()

    def _build_concept_graph(self):
        for concept in self.program.concepts:
            self.concept_graph[concept.name] = concept

    def _build_transform_index(self):
        self._transform_index: dict[str, TransformNode] = {}
        for t in self.program.transforms:
            key = tuple(sorted(t.cause))
            self._transform_index[key] = t

    def get_concept(self, name: str) -> ConceptNode:
        if name not in self.concept_graph:
            raise ConceptNotFoundError(name)
        return self.concept_graph[name]

    def execute_concept(self, name: str, **inputs: Any) -> Any:
        concept = self.get_concept(name)
        self._validate_inputs(concept, inputs)
        return self._evaluate_impl(concept, inputs)

    def _validate_inputs(self, concept: ConceptNode, inputs: dict[str, Any]):
        for param_name, param_type in concept.input_types:
            if param_name not in inputs:
                raise ConceptExecutionError(concept.name, f"Missing required input: {param_name}")

    def _evaluate_impl(self, concept: ConceptNode, inputs: dict[str, Any]) -> Any:
        impl = concept.impl
        if not impl:
            return None
        impl = self._substitute_inputs(impl, inputs)
        return self._execute_impl_string(concept, impl, inputs)

    def _substitute_inputs(self, impl: str, inputs: dict[str, Any]) -> str:
        for param_name, value in inputs.items():
            placeholder = f"{{{param_name}}}"
            if placeholder in impl:
                if isinstance(value, str):
                    impl = impl.replace(placeholder, value)
                else:
                    impl = impl.replace(placeholder, repr(value))
        return impl

    def _execute_impl_string(self, concept: ConceptNode, impl: str, inputs: dict[str, Any]) -> Any:
        local_vars = dict(inputs)
        try:
            result = eval(impl, {"__builtins__": __builtins__}, local_vars)
            return result
        except Exception as e:
            raise ConceptExecutionError(concept.name, f"Impl evaluation failed: {e}")

    def apply_transform(self, *cause_concepts: str) -> Optional[str]:
        key = tuple(sorted(cause_concepts))
        transform = self._transform_index.get(key)
        if not transform:
            return None
        self.transform_results[transform.name] = {
            "cause": cause_concepts,
            "applied": True,
        }
        return transform.effect

    def find_patterns(self, evidence: str) -> list[tuple[PatternNode, str]]:
        matches = []
        for pattern in self.program.patterns:
            if evidence.lower() in pattern.evidence.lower():
                matches.append((pattern, pattern.resolve))
        return matches

    def reason(self, query: str, context: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        context = context or {}
        results = {
            "query": query,
            "concepts_used": [],
            "transforms_applied": [],
            "patterns_matched": [],
            "result": None,
        }
        query_lower = query.lower()
        for concept in self.program.concepts:
            if concept.name.lower() in query_lower or query_lower in concept.reason.lower():
                results["concepts_used"].append(concept.name)
                if not concept.input_types or context:
                    try:
                        result = self.execute_concept(concept.name, **context)
                        results["result"] = result
                    except ConceptExecutionError:
                        pass
        patterns = self.find_patterns(query)
        for pattern, resolve in patterns:
            results["patterns_matched"].append({"name": pattern.name, "resolve": resolve})
        return results

    def explain_concept(self, name: str) -> str:
        concept = self.get_concept(name)
        lines = [
            f"CONCEPT: {concept.name}",
            f"  TYPE: {concept.concept_type}",
            f"  INPUT: {concept.input_types}",
            f"  OUTPUT: {concept.output_type}",
            f"  REASON: {concept.reason}",
            f"  IMPL: {concept.impl}",
        ]
        if concept.fields:
            lines.append(f"  FIELDS: {concept.fields}")
        return "\n".join(lines)

    def explain_relation(self, from_concept: str, to_concept: str) -> Optional[str]:
        for rel in self.program.relations:
            if rel.from_concept == from_concept and rel.to_concept == to_concept:
                return f"{rel.name} ({rel.relation_type}): {rel.reason}"
        return None

    def explain_transform(self, name: str) -> Optional[str]:
        for t in self.program.transforms:
            if t.name == name:
                return (f"TRANSFORM: {t.name}\n"
                        f"  CAUSE: {t.cause}\n"
                        f"  EFFECT: {t.effect}\n"
                        f"  PRESERVE: {t.preserve}\n"
                        f"  CONSTRAINT: {t.constraint}\n"
                        f"  MAP: {t.map}")
        return None

    def get_program_info(self) -> dict[str, int]:
        return {
            "num_concepts": len(self.program.concepts),
            "num_relations": len(self.program.relations),
            "num_transforms": len(self.program.transforms),
            "num_patterns": len(self.program.patterns),
        }


def reason(program: LinguaProgram) -> ReasoningEngine:
    return ReasoningEngine(program)