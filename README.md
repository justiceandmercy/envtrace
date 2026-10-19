# envtrace

Trace environment variable usage across a codebase: find every variable your code reads, compare it against your `.env` file, and surface variables that are used-but-undocumented or documented-but-unused.

## Features

- Scans source files in many languages (Python, JS/TS, Go, Rust, Ruby, PHP, Java, shell, YAML, ...) for common env-access patterns.
- Detects `process.env.X`, `process.env['X']`, `os.environ['X']`, `os.environ.get('X')`, `os.getenv('X')`, `getenv('X')`.
- Auto-detects a `.env` / `.env.example` / `.env.sample` file in the scanned root for comparison.
- Reports used variables with file counts, plus undocumented and unused sets.
- JSON output for CI integration.

## Install

```bash
git clone https://github.com/you/envtrace
cd envtrace
chmod +x envtrace.py
```

No external dependencies; requires Python 3.8+.

## Usage

```bash
# scan current directory
python3 envtrace.py .

# scan a project, comparing against an explicit env file
python3 envtrace.py ./myapp --env ./myapp/.env.example

# JSON output
python3 envtrace.py ./myapp --format json

# ignore extra directories
python3 envtrace.py . --ignore vendor --ignore generated
```

Example output:

```
Environment variables referenced in code: 5
  DATABASE_URL  (3 files)
  PORT  (1 file)
  API_KEY  (2 files)
  DEBUG  (1 file)
  LOG_LEVEL  (1 file)

Undocumented (used in code but not in env file): 1
  - LOG_LEVEL
Unused (in env file but not referenced in code): 1
  - LEGACY_FLAG
```

## License

MIT