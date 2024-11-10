# rapidchecker
Grammar and format checker for ABB Rapid code.

- 🔎 Checks ABB RAPID code (.sys modules) for grammar errors and formatting issues.
- 🦾 Tested with RobotWare 5 code.
- 🐍 Powered by Python and [pyparsing](https://github.com/pyparsing/pyparsing).

## Getting started

To install simply clone the repo and run `pip install .` .

Then check a module (or a folder of modules) by running

```bash
python -m rapidchecker <path-to-file>
```

If any grammar or format errors are found, they are printed to stdout and the command exits with exitcode 1.

## Features

`rapidchecker` checks for:

- Code that violates the ABB RAPID grammar.
- Bad indentation. Assumes indentation of 4 spaces.
- Lowercase keywords (`if` instead of `IF`, `module` instead of `MODULE` etc)

## To be added

- Add package to pip.
- CI
- Checks for procedure, variable, function and signal names (enforce camel_case or snakeCase).
