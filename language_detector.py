"""
Language Detection for Multi-Language Code Review
Automatically detects programming language from file extensions and content
"""

import re
from typing import Dict, List, Tuple
from collections import Counter
from utils import logger


class LanguageDetector:
    """Detect programming languages from file changes"""
    
    # File extension to language mapping
    EXTENSION_MAP = {
        # PHP/Laravel
        '.php': 'php',
        '.blade.php': 'php',
        
        # JavaScript/TypeScript
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'javascript',
        '.tsx': 'javascript',
        '.mjs': 'javascript',
        '.cjs': 'javascript',
        
        # Python
        '.py': 'python',
        '.pyw': 'python',
        '.pyi': 'python',
        
        # Configuration files
        '.json': 'config',
        '.yaml': 'config',
        '.yml': 'config',
        '.xml': 'config',
        '.toml': 'config',
    }
    
    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        'php': {
            'laravel': [
                r'Illuminate\\',
                r'use\s+Illuminate',
                r'Artisan::',
                r'Route::',
                r'@extends\(',
                r'@section\(',
            ],
        },
        'javascript': {
            'react': [
                r'from\s+[\'\']react[\'\']',
                r'import\s+React',
                r'useState',
                r'useEffect',
                r'<[A-Z]\w+',
                r'\.jsx?$',
            ],
            'angular': [
                r'@Component\(',
                r'@Injectable\(',
                r'@NgModule\(',
                r'from\s+[\'\']@angular',
                r'\.component\.ts$',
                r'\.service\.ts$',
            ],
            'vue': [
                r'<template>',
                r'<script>',
                r'from\s+[\'\']vue[\'\']',
                r'\.vue$',
            ],
            'node': [
                r'require\([\'\']',
                r'module\.exports',
                r'process\.env',
                r'express\(',
            ],
            'express': [
                r'require\([\'\']express[\'\']',
                r'app\.get\(',
                r'app\.post\(',
                r'app\.listen\(',
            ],
        },
        'python': {
            'django': [
                r'from\s+django',
                r'import\s+django',
                r'models\.Model',
                r'django\.conf',
            ],
            'flask': [
                r'from\s+flask',
                r'import\s+Flask',
                r'@app\.route',
            ],
            'fastapi': [
                r'from\s+fastapi',
                r'import\s+FastAPI',
                r'@app\.get',
                r'@app\.post',
            ],
        }
    }
    
    @staticmethod
    def detect_from_files(changed_files: List[str]) -> Tuple[str, str, Dict]:
        """Detect primary language and framework from changed files"""
        if not changed_files:
            return 'unknown', 'none', {}
        
        language_counter = Counter()
        
        # Count files by extension
        for filepath in changed_files:
            ext = LanguageDetector._get_extension(filepath)
            lang = LanguageDetector.EXTENSION_MAP.get(ext, 'other')
            
            if lang != 'config':
                language_counter[lang] += 1
        
        # Get primary language
        primary_language = language_counter.most_common(1)[0][0] if language_counter else 'unknown'
        
        stats = {
            'language_distribution': dict(language_counter),
            'total_files': len(changed_files),
            'primary_language': primary_language
        }
        
        return primary_language, 'none', stats
    
    @staticmethod
    def detect_framework_from_content(content: str, language: str) -> str:
        """Detect framework from code content"""
        if language not in LanguageDetector.FRAMEWORK_PATTERNS:
            return 'none'
        
        frameworks = LanguageDetector.FRAMEWORK_PATTERNS[language]
        framework_scores = Counter()
        
        for framework, patterns in frameworks.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, content, re.MULTILINE))
                if matches > 0:
                    framework_scores[framework] += matches
        
        return framework_scores.most_common(1)[0][0] if framework_scores else 'none'
    
    @staticmethod
    def detect_from_diff(diff_text: str, changed_files: List[str]) -> Tuple[str, str, Dict]:
        """Detect language and framework from diff and file list"""
        language, _, stats = LanguageDetector.detect_from_files(changed_files)
        framework = LanguageDetector.detect_framework_from_content(diff_text, language)
        stats['detected_framework'] = framework
        return language, framework, stats
    
    @staticmethod
    def _get_extension(filepath: str) -> str:
        """Get file extension"""
        filepath = filepath.lower()
        if filepath.endswith('.blade.php'):
            return '.blade.php'
        parts = filepath.split('.')
        return '.' + parts[-1] if len(parts) > 1 else ''
    
    @staticmethod
    def get_language_name(language: str, framework: str = 'none') -> str:
        """Get human-readable language/framework name"""
        names = {
            'php': 'PHP/Laravel' if framework == 'laravel' else 'PHP',
            'javascript': {
                'react': 'React',
                'angular': 'Angular',
                'vue': 'Vue.js',
                'node': 'Node.js',
                'express': 'Express.js',
                'none': 'JavaScript'
            }.get(framework, 'JavaScript'),
            'python': {
                'django': 'Django',
                'flask': 'Flask',
                'fastapi': 'FastAPI',
                'none': 'Python'
            }.get(framework, 'Python'),
            'unknown': 'Unknown'
        }
        return names.get(language, language.title())
