setup-rust:
    #!/usr/bin/env bash
    if ! which cargo > /dev/null; then
        echo "Installing Rust..."
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source ~/.cargo/env
    fi
    rustup update stable
    rustup default stable
    echo "✓ Rust $(rustc --version) ready"

setup-rust-python:
    uv --project rust_core tool install maturin
    uv --project rust_core sync

setup-test-python:
    uv --project python_app sync

setup: setup-rust setup-rust-python
    @echo "✓ Setup rust and rust-python complete"

build-develop:
    cd {{justfile_directory()}}/rust_core && uv run maturin develop
    cd {{justfile_directory()}}/python_app && uv sync

build-release:
    cd {{justfile_directory()}}/rust_core && uv run maturin build --release

test:
    cd {{justfile_directory()}}/python_app && uv run pytest tests/ -v
    @echo "✓ All tests passed"

fmt-rust:
    cd {{justfile_directory()}}/rust_core && cargo fmt

fmt-python:
    cd {{justfile_directory()}}/python_app && uv run ruff format src/ tests/

fmt: fmt-rust fmt-python

lint-rust:
    cd {{justfile_directory()}}/rust_core && cargo clippy -- -D warnings

lint-python:
    cd {{justfile_directory()}}/python_app && uv run ruff check src/ tests/

lint: lint-rust lint-python

check: fmt lint test
    @echo "✓ Project health check passed"

clean-rust:
    cd {{justfile_directory()}}/rust_core && cargo clean
    rm -rf {{justfile_directory()}}/rust_core/target

clean-python:
    rm -rf {{justfile_directory()}}/**/.venv
    rm -rf {{justfile_directory()}}/**/uv.lock
    find {{justfile_directory()}} -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find {{justfile_directory()}} -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find {{justfile_directory()}} -type f -name "*.pyc" -delete 2>/dev/null || true

clean: clean-rust clean-python

rebuild: clean setup build-release setup-test-python test
    @echo "✓ Rebuild complete"

inspect:
    @tree -I 'target|.venv|__pycache__|*.pyc|.pytest_cache|uv.lock' {{justfile_directory()}}
