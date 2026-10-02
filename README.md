# import-peek

Inventory static import declarations across Python files. It parses source with the standard-library AST and never executes it or prints source text.

Requires Python 3.8+ and uses only the standard library.

    python import_peek.py src/app.py src/util.py

Output is grouped by input file and module name. A from-module import of two names counts two references to that module. Relative imports are shown with their leading dots. Imports hidden behind runtime importlib calls are not detected.

Exit status: 0 when all files parse, 1 when at least one file has invalid Python syntax, 2 when one or more files could not be read.

## License

MIT. See [LICENSE](LICENSE).
