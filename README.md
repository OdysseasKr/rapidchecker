# rapidchecker
Grammar and format checker for ABB Rapid code.

- 🔎 Checks ABB RAPID code (.sys modules) for grammar errors and formatting issues.
- 🦾 Tested with RobotWare 5 code.
- 🐍 Powered by Python and [pyparsing](https://github.com/pyparsing/pyparsing).

## Getting started

Install with `pip install rapidchecker`

Then check a RAPID module (or a directory containing modules) by running

```bash
python -m rapidchecker <path-to-file-or-dir>
```

If any grammar or format errors are found, they are printed to stdout and the command exits with exitcode 1.

## Features

`rapidchecker` checks for:

- Code that violates the ABB RAPID grammar.
- Bad indentation. Assumes indentation of 4 spaces.
- Lowercase keywords (`if` instead of `IF`, `module` instead of `MODULE` etc)

## To be added

- Add package to pip.
- Checks for procedure, variable, function and signal names (enforce camel_case or snakeCase).

## References

- ABB RAPID [docs](https://library.e.abb.com/public/f23f1c3e506a4383b635cff165cc6993/3HAC050946+TRM+RAPID+Kernel+RW+6-en.pdf?x-sign=oUq9VZeSx%2Fve4%2BCCAYZVeAQoLxtMdzw6S2BkJobVIFhUVtPrZ8dmV1VIHdk%2B6Yfg)
- [PyParsing](https://pyparsing-docs.readthedocs.io/en/latest/)
