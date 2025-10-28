# Rust-Python Project

A Python package powered by Rust, featuring a text analysis library with PyO3 bindings.

## Project Structure

```
rust-py-project/
├── justfile                      # Main orchestration
├── rust_core/                    # Rust library → Python package
│   ├── Cargo.toml               # Rust dependencies
│   ├── pyproject.toml           # Maturin build config
│   ├── .python-version          # Python version (3.11)
│   └── src/
│       └── lib.rs               # TextAnalyzer implementation with PyO3
└── python_app/                   # Python project using rust_core
    ├── pyproject.toml           # Python dependencies + local rust_core
    ├── .python-version          # Python version (3.11)
    ├── src/
    │   └── python_app/
    │       └── __init__.py      # Python wrapper and utilities
    └── tests/
        ├── __init__.py
        └── test_integration.py  # Pytest integration tests
```

## Features

The `rust_core` package provides a `TextAnalyzer` class with:

- `word_count()` - Count word frequencies (case-insensitive, strips punctuation)
- `char_count()` - Count total characters including whitespace
- `most_common(n)` - Get top N most frequent words
- `get_text()` - Retrieve original text

## Quick Start

```bash
# Initial setup (installs Rust, maturin, rust_core deps)
just setup

# Build and install in development mode
just dev

# Run all tests
just test

# Format all code
just fmt

# Lint all code
just lint

# Clean and rebuild everything
just rebuild

# Check project health (format, lint, test)
just check
```

## Usage Example

```python
from rust_core import TextAnalyzer

# Create analyzer
analyzer = TextAnalyzer("The quick brown fox jumps over the lazy dog")

# Get word frequencies
counts = analyzer.word_count()
print(counts)  # {'the': 2, 'quick': 1, 'brown': 1, ...}

# Get character count
print(analyzer.char_count())  # 44

# Get top 3 most common words
top_words = analyzer.most_common(3)
print(top_words)  # [('the', 2), ('brown', 1), ('dog', 1)]
```

## Available Just Commands

**Setup:**
- `just setup` - Install Rust and rust_core dependencies
- `just setup-rust` - Install/update Rust toolchain
- `just setup-rust-python` - Install maturin and rust_core dependencies
- `just setup-test-python` - Sync python_app dependencies

**Build:**
- `just dev` - Build and install in development mode
- `just build-release` - Build optimized release wheel

**Testing:**
- `just test` - Run all tests

**Code Quality:**
- `just fmt` - Format all code
- `just fmt-rust` - Format Rust code
- `just fmt-python` - Format Python code
- `just lint` - Lint all code
- `just lint-rust` - Lint Rust code
- `just lint-python` - Lint Python code
- `just check` - Full health check (format + lint + test)

**Cleanup:**
- `just clean` - Remove all build artifacts
- `just clean-rust` - Remove Rust build artifacts
- `just clean-python` - Remove Python artifacts
- `just rebuild` - Clean and rebuild from scratch

**Utilities:**
- `just inspect` - Show project structure

## Requirements

- Rust (installed automatically by `just setup`)
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- [just](https://github.com/casey/just) command runner

## Development Workflow

1. Make changes to Rust code in `rust_core/src/lib.rs`
2. Run `just dev` to rebuild and install
3. Run `just test` to verify all tests pass
4. Format and lint with `just check`

## Architecture

- **rust_core**: Rust library compiled to a Python extension module using PyO3 and maturin
- **python_app**: Python application that depends on `rust_core` as an editable local dependency
- All state-changing operations are managed through the justfile for consistency
