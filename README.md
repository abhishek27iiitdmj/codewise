# 🤖 CodeWise - Multi-Language AI Code Reviewer

**Intelligent AI-powered code review for automated PR analysis across multiple languages**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Multi-Language](https://img.shields.io/badge/Languages-PHP%20%7C%20JavaScript%20%7C%20Python-brightgreen)](https://github.com/abhishek27iiitdmj/codewise)

CodeWise is an automated code review system that uses OpenAI GPT models to analyze pull requests and provide intelligent feedback on security, performance, best practices, and code quality. Now supports **PHP/Laravel**, **JavaScript/React/Angular/Node**, and **Python/Django/Flask/FastAPI**.

<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-brightgreen" alt="AI Powered"/>
  <img src="https://img.shields.io/badge/Security-First-red" alt="Security First"/>
  <img src="https://img.shields.io/badge/Multi--Language-Supported-blue" alt="Multi-Language"/>
</p>

---

## 🌟 What's New in v2.0

### ✨ Multi-Language Support
- **PHP/Laravel**: Security, Eloquent optimization, PSR-12 standards
- **JavaScript/TypeScript**: React, Angular, Vue, Node.js, Express
- **Python**: Django, Flask, FastAPI with PEP 8 compliance

### 🎯 Automatic Language Detection
- Detects programming language from file extensions
- Identifies frameworks (Laravel, React, Angular, Django, Flask, etc.)
- Provides language-specific feedback and best practices

### 🏗️ Modular Architecture
- Language-specific reviewers in separate modules
- Easy to extend with new languages
- Maintains backward compatibility with Laravel-only version

---

## 📋 Supported Languages & Frameworks

### 🐘 PHP
- **Language**: PHP 7.4+, PHP 8.x
- **Framework**: Laravel
- **Focus**: SQL injection, XSS, CSRF, Eloquent N+1 queries, Authorization, Validation

### ⚛️ JavaScript/TypeScript
- **Frameworks**: React, Angular, Vue.js, Node.js, Express.js
- **Focus**: XSS, Prototype pollution, Memory leaks, React Hooks, Async patterns, Bundle optimization

### 🐍 Python
- **Frameworks**: Django, Flask, FastAPI
- **Focus**: SQL injection, Command injection, ORM optimization, Type hints, PEP 8, Async/await

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/abhishek27iiitdmj/codewise.git
cd codewise
./setup.sh
```

### Configuration

1. **Copy environment template:**
```bash
cp .env.example .env
```

2. **Set required variables in `.env`:**
```bash
BITBUCKET_WORKSPACE=<your-workspace>
BITBUCKET_REPO_SLUG=<your-repo>
BITBUCKET_PR_ID=<pr-number>
BITBUCKET_APP_PASSWORD=<your-app-password>
OPENAI_KEY=<your-openai-api-key>
```

3. **Configure languages (optional):**
Edit `config_multilang.yaml` to enable/disable languages or customize settings.

### Run Review

**Multi-Language (Auto-detect):**
```bash
source venv/bin/activate
python ai_reviewer_multilang.py
```

**Or use the executable:**
```bash
./codewise-multilang
```

**Legacy Laravel-only:**
```bash
python ai_reviewer.py  # Original Laravel-specific version
```

---

## 🏗️ Project Structure

```
codewise/
├── ai_reviewer_multilang.py   # Multi-language main entry point
├── ai_reviewer.py              # Legacy Laravel-specific version
├── language_detector.py        # Auto-detect programming language
├── base_reviewer.py            # Abstract base for all reviewers
├── reviewer_factory.py         # Factory to create language reviewers
├── languages/                  # Language-specific modules
│   ├── php/
│   │   ├── __init__.py
│   │   └── php_reviewer.py    # PHP/Laravel reviewer
│   ├── javascript/
│   │   ├── __init__.py
│   │   └── javascript_reviewer.py  # JS/React/Angular/Node
│   └── python/
│       ├── __init__.py
│       └── python_reviewer.py # Python/Django/Flask
├── clients.py                  # Bitbucket & OpenAI API clients
├── filters.py                  # Diff filtering
├── formatters.py               # Comment formatting
├── enhancements.py             # Advanced features
├── utils.py                    # Utilities
├── config_multilang.yaml       # Multi-language configuration
├── config.yaml                 # Legacy configuration
└── requirements.txt            # Dependencies
```

---

## ⚙️ Configuration

### Multi-Language Config (`config_multilang.yaml`)

```yaml
# OpenAI Model
model: "gpt-3.5-turbo"
temperature: 0.2
max_tokens: 2000

# Language-Specific Settings
languages:
  php:
    enabled: true
    frameworks: [laravel]
    focus_areas: [security, performance, eloquent_optimization]
  
  javascript:
    enabled: true
    frameworks: [react, angular, vue, node, express]
    focus_areas: [security, performance, accessibility]
  
  python:
    enabled: true
    frameworks: [django, flask, fastapi]
    focus_areas: [security, performance, type_hints]
```

---

## 🎯 How It Works

### 1. **Language Detection**
```
Changed Files → Language Detector → Primary Language + Framework
```
- Analyzes file extensions (`.php`, `.js`, `.py`)
- Detects frameworks from code patterns
- Handles mixed-language PRs (uses primary language)

### 2. **Reviewer Selection**
```
Language + Framework → Reviewer Factory → Specialized Reviewer
```
- Creates language-specific reviewer instance
- Loads appropriate best practices and security rules
- Generates specialized review prompts

### 3. **AI Analysis**
```
Specialized Prompt → OpenAI GPT → Language-Specific Review
```
- Security vulnerabilities
- Performance issues
- Framework-specific anti-patterns
- Best practice violations

### 4. **Enhanced Feedback**
```
Review + Confidence Score + Learning Resources → Bitbucket Comment
```

---

## 📊 Review Categories

### 🔴 Critical Issues
- **PHP**: SQL injection, XSS, mass assignment, authorization bypass
- **JavaScript**: Prototype pollution, XSS, command injection, JWT vulnerabilities
- **Python**: SQL injection, command injection, pickle vulnerabilities, path traversal

### 🟡 Important Issues
- **PHP**: N+1 queries, missing validation, performance bottlenecks
- **JavaScript**: Memory leaks, inefficient React patterns, unoptimized bundles
- **Python**: ORM inefficiencies, missing type hints, exception handling

### 🔵 Suggestions
- **PHP**: PSR-12 compliance, code organization, documentation
- **JavaScript**: Modern ES6+ syntax, accessibility improvements
- **Python**: PEP 8 compliance, Pythonic patterns, docstrings

---

## 🔍 Language-Specific Features

### PHP/Laravel
✅ Eloquent query optimization  
✅ Authorization policy checks  
✅ Blade template security  
✅ Mass assignment protection  
✅ CSRF token validation  

### JavaScript/React/Angular
✅ React Hooks best practices  
✅ Component performance optimization  
✅ XSS prevention in JSX  
✅ Async/await error handling  
✅ Bundle size optimization  
✅ Angular dependency injection  

### Python/Django/Flask
✅ ORM N+1 detection  
✅ Type hints validation  
✅ Django security middleware  
✅ FastAPI async patterns  
✅ PEP 8 compliance  

---

## 💡 Examples

### Multi-Language PR Detection

**Input:** PR with mixed files
```
src/backend/api.py         # Python
src/backend/models.py      # Python  
frontend/App.jsx           # React
frontend/hooks/useAuth.js  # JavaScript
```

**Output:**
```
🤖 Detected language: Python
📊 Language distribution:
   - python: 2 files
   - javascript: 2 files
```

### Framework Detection

**Laravel Detection:**
```php
use Illuminate\Support\Facades\Route;
Route::get('/users', [UserController::class, 'index']);
```
→ Detected: **Laravel**

**React Detection:**
```javascript
import React, { useState, useEffect } from 'react';
function UserProfile() { ... }
```
→ Detected: **React**

**Django Detection:**
```python
from django.db import models
class User(models.Model):
```
→ Detected: **Django**

---

## 🔧 Advanced Usage

### Custom Language Configuration

```yaml
languages:
  javascript:
    enabled: true
    frameworks: [react]  # Review only React code
    focus_areas: [security, performance]  # Skip accessibility
```

### Disable Language Support

```yaml
languages:
  python:
    enabled: false  # Skip Python files in review
```

### Mixed-Language PRs

CodeWise automatically handles PRs with multiple languages:
1. Detects primary language (most files)
2. Uses appropriate reviewer
3. Displays language distribution in comment

---

## 📈 Backward Compatibility

### Laravel-Only Mode

The original Laravel-specific reviewer is preserved:

```bash
# Use original Laravel-specific version
python ai_reviewer.py
```

This ensures existing CI/CD pipelines continue working unchanged.

---

## 🚀 CI/CD Integration

### Bitbucket Pipelines

```yaml
pipelines:
  pull-requests:
    '**':
      - step:
          name: AI Code Review (Multi-Language)
          image: python:3.11
          script:
            - pip install -r requirements.txt
            - python ai_reviewer_multilang.py
```

---

## 🛠️ Extending with New Languages

### 1. Create Language Reviewer

```python
# languages/golang/golang_reviewer.py
from base_reviewer import BaseReviewer

class GoReviewer(BaseReviewer):
    def get_language(self) -> str:
        return "golang"
    
    def get_system_prompt(self, framework=None) -> str:
        return """Expert Go code reviewer..."""
    
    def get_focus_areas(self) -> List[str]:
        return ['security', 'concurrency', 'error_handling']
    
    def get_common_issues(self) -> Dict:
        return { ... }
```

### 2. Register in Factory

```python
# reviewer_factory.py
from languages.golang.golang_reviewer import GoReviewer

REVIEWER_MAP = {
    'golang': GoReviewer,
    # ...
}
```

### 3. Add to Language Detector

```python
# language_detector.py
EXTENSION_MAP = {
    '.go': 'golang',
    # ...
}
```

---

## 📝 Migration Guide

### From Laravel-Only to Multi-Language

**Before (v1.0):**
```bash
python ai_reviewer.py  # Laravel only
```

**After (v2.0):**
```bash
python ai_reviewer_multilang.py  # Auto-detects language
```

**Configuration:**
- Replace `config.yaml` with `config_multilang.yaml`
- No code changes required
- Language detection is automatic

---

## 🐛 Troubleshooting

### Language Not Detected
**Solution:** Check file extensions and ensure language is enabled in config.

### Wrong Framework Detected
**Solution:** Improve framework patterns in `language_detector.py`.

### Mixed Language PRs
**Solution:** Configure primary language manually or split PRs by language.

---

## 📊 Cost & Performance

- **PHP/Laravel PR**: ~$0.004 per review
- **JavaScript/React PR**: ~$0.005 per review
- **Python/Django PR**: ~$0.004 per review
- **Review Time**: <3 minutes per PR
- **Scalability**: Handles PRs up to 5000 lines

---

## 🤝 Contributing

We welcome contributions for new languages and improvements!

1. Fork the repository
2. Create language reviewer in `languages/<language>/`
3. Implement `BaseReviewer` interface
4. Add tests
5. Submit pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- OpenAI GPT models for AI-powered reviews
- Bitbucket API for PR integration
- The open-source community for inspiration

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/abhishek27iiitdmj/codewise/issues)
- **GitHub**: [abhishek27iiitdmj/codewise](https://github.com/abhishek27iiitdmj/codewise)
- **Documentation**: See docs/ folder

---

**CodeWise v2.0** - Making code reviews intelligent, consistent, and language-aware! 🚀
