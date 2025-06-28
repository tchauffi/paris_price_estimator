.PHONY: help install install-dev setup pre-commit lint format check test clean build

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install all dependencies including dev"
	@echo "  setup        - Complete project setup (install + pre-commit)"
	@echo "  pre-commit   - Install pre-commit hooks"
	@echo "  lint         - Run ruff linter"
	@echo "  format       - Run ruff formatter"
	@echo "  check        - Run both linting and formatting checks"
	@echo "  test         - Run tests (when available)"
	@echo "  clean        - Clean build artifacts and cache"
	@echo "  build        - Build the package"

# Install production dependencies only
install:
	poetry install --only=main

# Install all dependencies including dev
install-dev:
	poetry install

# Complete project setup
setup: install-dev pre-commit
	@echo "Project setup complete!"

# Install pre-commit hooks
pre-commit:
	poetry run pre-commit install
	@echo "Pre-commit hooks installed!"

# Run ruff linter
lint:
	poetry run ruff check .

# Run ruff formatter
format:
	poetry run ruff format .

# Run both linting and formatting
check: lint
	poetry run ruff check . --diff
	poetry run ruff format . --check

# Run tests (placeholder for when tests are added)
test:
	@echo "No tests configured yet"
	# poetry run pytest

# Clean build artifacts and cache
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build the package
build: clean
	poetry build

# Update dependencies
update:
	poetry update

# Run pre-commit on all files
pre-commit-all:
	poetry run pre-commit run --all-files
