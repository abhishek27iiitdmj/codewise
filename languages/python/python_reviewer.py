"""
Python Code Reviewer
Specialized reviewer for Python applications including Django, Flask, and FastAPI
"""

from typing import Dict, List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_reviewer import BaseReviewer


class PythonReviewer(BaseReviewer):
    """Python code reviewer"""
    
    def get_language(self) -> str:
        return "python"
    
    def get_system_prompt(self, framework: Optional[str] = None) -> str:
        """Generate system prompt for Python review"""
        
        base_prompt = """You are an expert Python code reviewer specializing in:
- Security vulnerabilities (SQL injection, command injection, path traversal, pickle vulnerabilities)
- Python best practices and PEP 8 style guide
- Performance optimization (algorithmic efficiency, memory usage, database queries)
- Code quality and maintainability
- Type hints and static typing
- Error handling and exception management
"""
        
        prompt = base_prompt
        prompt += """
Analyze the code changes and provide a structured review with:
1. 🔴 Critical Issues - Security vulnerabilities, breaking changes, data corruption risks
2. 🟡 Important Issues - Performance problems, anti-patterns, potential bugs
3. 🔵 Suggestions - Code quality improvements, Pythonic patterns, readability

For each issue:
- Provide specific file and line references
- Explain the problem clearly and its impact
- Suggest concrete fixes with Pythonic code examples
- Be concise but thorough
- Rate your confidence (High/Medium/Low)

Focus on:
- Security vulnerabilities (injection attacks, insecure deserialization)
- Performance bottlenecks (inefficient algorithms, database queries)
- Pythonic code patterns and idioms
- Proper exception handling
- Type safety and type hints
- Resource management (file handles, database connections)
- Testing and testability

Format your response in clean markdown."""
        
        return prompt
    
    def get_focus_areas(self) -> List[str]:
        return [
            'security',
            'performance',
            'best_practices',
            'pythonic_code',
            'type_hints',
            'error_handling',
            'code_quality',
            'testing'
        ]
    
    def get_common_issues(self) -> Dict[str, Dict]:
        """Return dictionary of common Python issues"""
        return {}
