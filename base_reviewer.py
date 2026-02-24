"""
Base Reviewer Class for Multi-Language Code Review
Provides abstract interface that all language-specific reviewers must implement
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class BaseReviewer(ABC):
    """Abstract base class for language-specific reviewers"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.language = self.get_language()
        self.framework = 'none'
    
    @abstractmethod
    def get_language(self) -> str:
        """Return the language this reviewer handles"""
        pass
    
    @abstractmethod
    def get_system_prompt(self, framework: Optional[str] = None) -> str:
        """
        Generate system prompt for AI review
        Should include language-specific best practices, security concerns, etc.
        """
        pass
    
    @abstractmethod
    def get_focus_areas(self) -> List[str]:
        """
        Return list of focus areas for this language
        Example: ['security', 'performance', 'best_practices']
        """
        pass
    
    @abstractmethod
    def get_common_issues(self) -> Dict[str, Dict]:
        """
        Return dictionary of common issues and their learning resources
        Format: {
            'issue_key': {
                'title': 'Issue Title',
                'description': 'Description',
                'url': 'Learning resource URL',
                'severity': 'critical|important|suggestion'
            }
        }
        """
        pass
    
    def format_user_prompt(
        self, 
        pr_details: Dict, 
        diff: str, 
        full_files: Optional[Dict[str, str]] = None,
        framework: Optional[str] = None
    ) -> str:
        """
        Format user prompt with PR context
        Can be overridden by subclasses for custom formatting
        """
        prompt = f"""Review the following pull request changes:

**Repository:** {pr_details.get('source', {}).get('repository', {}).get('full_name', 'N/A')}
**PR #{pr_details.get('id')}:** {pr_details.get('title', 'N/A')}
**Author:** {pr_details.get('author', {}).get('display_name', 'N/A')}
**Language:** {self.get_language().title()}"""

        if framework and framework != 'none':
            prompt += f"\n**Framework:** {framework.title()}"
        
        prompt += f"""

**CODE DIFF:**
```diff
{diff[:15000]}
```
"""
        
        # Add full file context if available
        if full_files:
            prompt += "\n\n**FULL FILE CONTEXT (for better understanding):**\n"
            for filepath, content in full_files.items():
                # Truncate large files
                content_preview = content[:5000] if len(content) > 5000 else content
                ext = filepath.split('.')[-1]
                prompt += f"\n```{ext}\n// File: {filepath}\n{content_preview}\n```\n"
        
        prompt += f"\nProvide a structured code review focusing on {self.get_language().title()} security and best practices."
        return prompt
    
    def get_severity_icon(self, severity: str) -> str:
        """Get emoji icon for severity level"""
        icons = {
            'critical': '🔴',
            'important': '🟡',
            'suggestion': '🔵',
            'info': '⚪'
        }
        return icons.get(severity, '⚪')
    
    def enhance_review_with_resources(self, review_content: str) -> List[Dict]:
        """
        Analyze review content and suggest relevant learning resources
        """
        resources = []
        common_issues = self.get_common_issues()
        review_lower = review_content.lower()
        
        for issue_key, issue_data in common_issues.items():
            # Check if issue keywords appear in review
            keywords = issue_data.get('keywords', [issue_key.replace('_', ' ')])
            for keyword in keywords:
                if keyword.lower() in review_lower:
                    resources.append({
                        'title': issue_data['title'],
                        'url': issue_data['url'],
                        'description': issue_data.get('description', '')
                    })
                    break
        
        return resources
