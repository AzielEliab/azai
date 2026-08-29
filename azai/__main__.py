"""Allow ``python -m azai`` to invoke the CLI."""

from azai.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
