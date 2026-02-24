"""
JavaScript/Node.js/React/Angular Code Reviewer
Specialized reviewer for JavaScript ecosystem
"""

from typing import Dict, List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_reviewer import BaseReviewer


class JavaScriptReviewer(BaseReviewer):
    """JavaScript, Node.js, React, and Angular code reviewer"""
    
    def get_language(self) -> str:
        return "javascript"
    
    def get_system_prompt(self, framework: Optional[str] = None) -> str:
        """Generate system prompt for JavaScript review"""
        
        base_prompt = """You are an expert JavaScript/TypeScript code reviewer specializing in:
- Security vulnerabilities (XSS, injection attacks, prototype pollution, dependency vulnerabilities)
- Modern JavaScript/ES6+ best practices
- Performance optimization (bundle size, rendering, memory leaks)
- Code quality and maintainability
- Error handling and async/await patterns
"""
        
        prompt = base_prompt
        prompt += """
Analyze the code changes and provide a structured review with:
1. 🔴 Critical Issues - Security vulnerabilities, breaking changes, severe bugs
2. 🟡 Important Issues - Performance problems, anti-patterns, potential bugs
3. 🔵 Suggestions - Code quality improvements, modern syntax usage, readability

For each issue:
- Provide specific file and line references
- Explain the problem clearly and its impact
- Suggest concrete fixes with code examples
- Be concise but thorough
- Rate your confidence (High/Medium/Low)

Format your response in clean markdown."""
        
        return prompt
    
    def get_focus_areas(self) -> List[str]:
        return [
            'security',
            'performance',
            'best_practices',
            'async_patterns',
            'error_handling',
            'code_quality',
            'accessibility',
            'testing'
        ]
    
    def get_common_issues(self) -> Dict[str, Dict]:
        """Return dictionary of common JavaScript issues"""
        return {}
