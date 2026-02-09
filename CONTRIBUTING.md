# Contributing to OpenPartSelector

Thank you for your interest in contributing! This document provides guidelines and instructions.

## 🤝 How to Contribute

### 1. Fork the Repository
Fork this repo on GitHub, then clone your fork locally:

```bash
git clone https://github.com/YOUR-USERNAME/OpenPartSelector.git
cd OpenPartSelector
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt
```

### 3. Make Changes

- Create a new branch: `git checkout -b feature/amazing-feature`
- Make your changes following our coding standards
- Add tests for your changes
- Run tests: `pytest`

### 4. Coding Standards

We use:
- **Black** for code formatting
- **isort** for import sorting
- **mypy** for type checking
- **pytest** for testing

```bash
# Format code
black .
isort .

# Type check
mypy .

# Run tests
pytest tests/ -v
```

### 5. Submit a Pull Request

Push your changes and create a PR on GitHub.

## 📝 Guidelines

- Write clear, commented code
- Add docstrings to new functions/classes
- Update documentation for new features
- Keep pull requests focused (one feature per PR)
- Write tests for bug fixes and new features

## 🐛 Reporting Bugs

Open an issue with:
- Clear title
- Steps to reproduce
- Expected vs actual behavior
- Environment details

## 💡 Feature Requests

Open an issue with:
- Clear description of the feature
- Use case / why it's useful
- Possible implementation approach (optional)

---

**Thank you for contributing!** 🎉
