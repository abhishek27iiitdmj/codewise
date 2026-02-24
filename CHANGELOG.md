# CodeWise Changelog

## [2.0.0] - 2026-02-12

### 🎉 Major Release - Multi-Language Support

#### Added
- **Multi-language support**: PHP, JavaScript, Python
- **Automatic language detection** from file extensions
- **Framework detection**: Laravel, React, Angular, Vue, Node.js, Express, Django, Flask, FastAPI
- Language-specific reviewers with specialized prompts
- Base reviewer abstraction for easy language extension
- Reviewer factory pattern for creating language-specific reviewers
- Language-specific learning resources and documentation links
- Support for mixed-language PRs (uses primary language)

#### Changed
- **BREAKING**: `ai_reviewer.py` is now multi-language by default (was Laravel-only)
- **BREAKING**: `config.yaml` now includes multi-language settings
- Unified all language functionality into single entry point
- Updated `codewise` executable to use multi-language version
- Enhanced comment formatting to show detected language
- README now focuses on multi-language capabilities

#### Removed
- Separate Laravel-only entry point (functionality preserved in PHP reviewer)
- `prompts.py` (prompts now in language-specific reviewers)
- `codewise-multilang` (redundant, main script is now multi-language)

#### Architecture
- New modular structure with `languages/` directory:
  - `languages/php/php_reviewer.py` - PHP/Laravel specialist
  - `languages/javascript/javascript_reviewer.py` - JavaScript/TypeScript specialist
  - `languages/python/python_reviewer.py` - Python specialist
- `base_reviewer.py` - Abstract base for all reviewers
- `language_detector.py` - Automatic language/framework detection
- `reviewer_factory.py` - Factory for creating reviewers

#### Backward Compatibility
- Legacy Laravel-only files backed up as `*.bak`
- Can restore Laravel-only mode by restoring backup files
- All original Laravel functionality preserved in PHP reviewer

#### Migration
- No action required - automatic language detection works out of the box
- Optional: Update CI/CD to leverage multi-language support
- Optional: Configure enabled languages in `config.yaml`

---

## [1.0.0] - Previous Release

### Features
- Laravel/PHP code review
- Bitbucket integration
- OpenAI GPT-3.5/4 support
- Cost tracking
- Multi-file context
- Confidence scoring
- Learning resources
- Similarity search

---

**For detailed migration information, see MIGRATION.md**
