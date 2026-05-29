# Contributing to A-Stock ESG Framework

Thank you for your interest in contributing to the A-Stock ESG Framework! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub with:

- A clear description of the problem or suggestion
- Steps to reproduce (for bugs)
- Expected vs actual behavior

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for public functions
- Keep functions focused and concise

### Testing

- Write tests for new features
- Ensure all existing tests pass
- Aim for good test coverage

## Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/a-stock-esg-framework.git
cd a-stock-esg-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_framework.py
```

## Code Quality

```bash
# Format code
black src/ tests/

# Check for style issues
flake8 src/ tests/

# Type checking
mypy src/
```

## Questions?

If you have questions about contributing, feel free to open an issue or reach out to the maintainers.
