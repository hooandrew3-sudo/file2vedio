# Contributing to File2Vedio

Thank you for your interest in contributing to File2Vedio! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project and everyone participating in it is governed by a Code of Conduct. By participating, you are expected to uphold this code.

## How to Contribute

### 1. Report Bugs

Before creating bug reports, please check the existing issues list to avoid duplicates.

**When creating a bug report include:**
- Clear descriptive title
- Detailed description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)
- Screenshots/logs if applicable

### 2. Suggest Enhancements

Enhancement suggestions are tracked as GitHub issues.

**Include:**
- Clear descriptive title
- Detailed description of suggested enhancement
- Possible implementation approach
- Examples of similar features

### 3. Pull Requests

- Fork the repository
- Create a new branch (`git checkout -b feature/amazing-feature`)
- Commit changes (`git commit -m 'Add amazing feature'`)
- Push to branch (`git push origin feature/amazing-feature`)
- Open a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/file2vedio.git
cd file2vedio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make setup
# or
pip install -r requirements.txt
cp .env.example .env

# Run development server
make dev
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Max line length: 120 characters
- Use meaningful variable and function names

### Format Code

```bash
make format  # Uses black
```

### Lint Code

```bash
make lint    # Uses flake8
```

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Refactor, etc.)
- Keep first line under 50 characters
- Add detailed explanation in body if needed

Example:
```
Add text processing for Chinese content

Implements automatic text cleaning and sentence segmentation
for Chinese articles. Adds support for character-based duration
estimation.
```

## Testing

```bash
make test    # Run all tests
python -m pytest tests.py -v  # Verbose output
python -m pytest tests.py::TestTextProcessor  # Specific test class
```

## Documentation

- Update README.md for significant changes
- Add docstrings to new functions/classes
- Include type hints where applicable
- Update QUICKSTART.md for user-facing features

## Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring
- `test/description` - Tests

## Pull Request Process

1. Update README.md and QUICKSTART.md with changes
2. Add tests for new functionality
3. Ensure all tests pass: `make test`
4. Ensure code is formatted: `make format`
5. Ensure code passes linting: `make lint`
6. Update version numbers if applicable
7. Provide clear PR description

## License

By contributing to File2Vedio, you agree that your contributions will be licensed under its MIT License.

## Questions?

Feel free to open an issue with the `question` label.

Thank you for contributing! 🎉
