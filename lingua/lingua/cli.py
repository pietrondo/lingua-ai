"""LINGUA CLI - Command line interface."""

import sys
from pathlib import Path
from lingua import parse, generate_python, generate_json, generate_ir, reason as reason_engine, ReasoningEngine


def main():
    args = sys.argv[1:]

    if not args or "-h" in args or "--help" in args:
        print("LINGUA - AI-optimized programming language")
        print("Usage: lingua <command> [options]")
        print("")
        print("Commands:")
        print("  parse <file>      Parse and display AST")
        print("  python <file>     Generate Python code")
        print("  json <file>       Generate JSON representation")
        print("  ir <file>         Generate intermediate representation")
        print("  reason <file> <query> [key=value ...]")
        print("                    Query the knowledge graph")
        print("")
        print("Options:")
        print("  -h, --help        Show this help")
        return 0

    command = args[0]
    if command not in ("parse", "python", "json", "ir", "reason"):
        print(f"Unknown command: {command}")
        return 1

    if len(args) < 2:
        print(f"Usage: lingua {command} <file>")
        return 1

    filepath = Path(args[1])
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return 1

    source = filepath.read_text(encoding="utf-8")

    try:
        program = parse(source)

        if command == "parse":
            print(f"Parsed {len(program.concepts)} concepts, {len(program.relations)} relations, "
                  f"{len(program.transforms)} transforms, {len(program.patterns)} patterns")
        elif command == "python":
            print(generate_python(program))
        elif command == "json":
            print(generate_json(program))
        elif command == "ir":
            import json
            print(json.dumps(generate_ir(program), indent=2))
        elif command == "reason":
            import json
            if len(args) < 3:
                print("Usage: lingua reason <file> <query> [key=value ...]")
                return 1
            query = args[2]
            context = {}
            for arg in args[3:]:
                if "=" in arg:
                    key, value = arg.split("=", 1)
                    try:
                        context[key] = json.loads(value)
                    except json.JSONDecodeError:
                        context[key] = value
            engine = reason_engine(program)
            result = engine.reason(query, context)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())