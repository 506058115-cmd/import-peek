#!/usr/bin/env python3
"""Inventory static Python import declarations without executing source files."""

import argparse
import ast
import sys
import tokenize
from collections import Counter
from pathlib import Path


class ImportCollector(ast.NodeVisitor):
    def __init__(self):
        self.modules = Counter()

    def visit_Import(self, node):
        for item in node.names:
            self.modules[item.name] += 1
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = "." * node.level + (node.module or "")
        self.modules[module or "(current package)"] += len(node.names)
        self.generic_visit(node)


def inspect(path):
    with tokenize.open(str(path)) as source:
        tree = ast.parse(source.read(), filename=str(path))
    collector = ImportCollector()
    collector.visit(tree)
    return collector.modules


def main():
    parser = argparse.ArgumentParser(
        description="List static Python imports without executing files or printing source."
    )
    parser.add_argument("files", nargs="+", type=Path, help="Python source files to inspect")
    args = parser.parse_args()
    syntax_failed = False
    read_failed = False

    for path in args.files:
        try:
            modules = inspect(path)
        except SyntaxError as error:
            line = error.lineno if error.lineno is not None else "?"
            print(f"import-peek: {path}:{line}: cannot parse Python: {error.msg}", file=sys.stderr)
            syntax_failed = True
            continue
        except (OSError, UnicodeError) as error:
            print(f"import-peek: {path}: cannot read Python source: {error}", file=sys.stderr)
            read_failed = True
            continue

        total = sum(modules.values())
        print(f"{path}: {total} static import reference(s)")
        if not modules:
            print("  (no static imports)")
        else:
            for module, count in sorted(modules.items()):
                print(f"  {module}: {count}")

    if read_failed:
        return 2
    return 1 if syntax_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
