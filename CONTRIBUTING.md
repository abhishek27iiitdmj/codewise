# Contributing to CodeWise

Thank you for your interest in contributing to CodeWise! We welcome contributions from everyone. This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We're committed to providing a welcoming and inclusive environment.

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check the [issue list](https://github.com/abhishek27iiitdmj/codewise/issues) as you might find out that you don't need to create one. When creating a bug report, include:

- **Clear description** of what the bug is
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Screenshots or logs** (if applicable)
- **Your environment** (Python version, AWS region, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear, descriptive title**
- **Provide a step-by-step description** of the suggested enhancement
- **Provide specific examples** to demonstrate the steps
- **Describe the current behavior** and **explain the expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Follow the coding style of the project (see style guide below)
- Test your changes locally
- Write clear, descriptive commit messages
- Reference any related issues in your PR description
- Update documentation if needed

## Development Setup

```bash
# Clone the repository
git clone https://github.com/abhishek27iiitdmj/codewise.git
cd codewise

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest black pylint
```

## Local Testing

```bash
# Test Lambda locally
sam build --use-container
sam local invoke CodeWiseFunction --event test-event-local.json

# Run tests
pytest

# Format code
black .

# Lint code
pylint **/*.py
```

## Code Style Guide

- **Python**: Follow [PEP 8](https://pep8.org/) style guide
- **Format with** `black` before committing
- **Docstrings**: Use triple quotes for all functions and classes
- **Type hints**: Include type hints for function parameters and returns
- **Comments**: Keep comments clear and concise

Example:

```python
def analyze_code(pr_diff: str, model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
    """
    Analyze PR diff using OpenAI model.
    
    Args:
        pr_diff: The diff content to analyze
        model: OpenAI model to use (default: gpt-3.5-turbo)
        
    Returns:
        Dictionary containing analysis results
    """
```

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 50 characters
- Reference issues using `#issue-number`

Examples:
```
Fix authentication error in Bitbucket client #123
Add support for multi-file context analysis
Update README with new deployment instructions
```

## Testing

- Write tests for new features
- Ensure all tests pass: `pytest`
- Aim for >80% code coverage
- Test both successful and error cases

## Documentation

- Update README.md for user-facing changes
- Update DEPLOYMENT.md for deployment changes
- Add docstrings to new functions and classes
- Update type hints and signatures

## Project Structure

```
codewise/
├── ai_reviewer.py          # Main review orchestration
├── clients.py              # Bitbucket and OpenAI clients
├── config.py               # Configuration management
├── filters.py              # Diff filtering logic
├── formatters.py           # Comment formatting
├── prompts.py              # AI prompt templates
├── enhancements.py         # Advanced features
├── utils.py                # Utility functions
├── lambda_handler.py       # AWS Lambda entry point
├── config.yaml             # Configuration file
├── template.yaml           # SAM template
├── Dockerfile              # Container image
├── requirements.txt        # Python dependencies
├── README.md               # User documentation
├── DEPLOYMENT.md           # Deployment guide
└── docs/                   # Additional documentation
```

## Key Components

### ai_reviewer.py
Main orchestration logic that:
- Fetches PR details from Bitbucket
- Analyzes code using OpenAI
- Posts review comments back

### clients.py
- `BitbucketClient`: Handles Bitbucket API interactions
- `OpenAIClient`: Handles OpenAI API calls

### enhancements.py
Advanced features:
- Multi-file context analysis
- Confidence scoring
- Learning resources
- Similarity search

### filters.py
Smart filtering to exclude:
- Vendor directories
- Generated files
- Large files
- Binary files

## Review Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test locally: `sam local invoke ...`
5. Format code: `black .`
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

### PR Checklist

- [ ] Tests pass locally
- [ ] Code formatted with `black`
- [ ] No security issues
- [ ] Documentation updated
- [ ] Clear commit messages
- [ ] References related issues

## Areas for Contribution

We're looking for help with:

- 🐛 Bug fixes
- ✨ New language support (Go, Rust, Java, etc.)
- 📚 Documentation improvements
- 🧪 Test coverage improvements
- ⚡ Performance optimizations
- 🔒 Security enhancements
- 🎨 UI/UX improvements for output
- 📊 Analytics and metrics

## Performance Considerations

When contributing, consider:

- Execution time (target <2 minutes per PR)
- Token usage and cost
- Memory usage on Lambda (1GB limit)
- API call efficiency

## Security

- Never commit API keys or secrets
- Use environment variables for credentials
- Review `.gitignore` for sensitive patterns
- Don't log sensitive information
- Use `sanitize_log()` for logs

## Questions?

- Open a [GitHub Discussion](https://github.com/abhishek27iiitdmj/codewise/discussions)
- Check [existing issues](https://github.com/abhishek27iiitdmj/codewise/issues)
- Review [documentation](https://github.com/abhishek27iiitdmj/codewise/blob/main/README.md)

---

Thank you for contributing to CodeWise! 🎉
