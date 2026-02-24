"""
Reviewer Factory
Factory pattern to create appropriate reviewer based on detected language
"""

import sys
import os
from typing import Dict, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_reviewer import BaseReviewer
from languages.php.php_reviewer import PHPReviewer
from languages.javascript.javascript_reviewer import JavaScriptReviewer
from languages.python.python_reviewer import PythonReviewer
from utils import logger


class ReviewerFactory:
    """Factory for creating language-specific reviewers"""
    
    # Map languages to their reviewer classes
    REVIEWER_MAP = {
        'php': PHPReviewer,
        'javascript': JavaScriptReviewer,
        'python': PythonReviewer,
    }
    
    @staticmethod
    def create_reviewer(language: str, config: Dict) -> Optional[BaseReviewer]:
        """Create appropriate reviewer based on language"""
        reviewer_class = ReviewerFactory.REVIEWER_MAP.get(language.lower())
        
        if not reviewer_class:
            logger.warning(f"No reviewer available for language: {language}")
            return None
        
        logger.info(f"Creating {language} reviewer")
        return reviewer_class(config)
    
    @staticmethod
    def get_supported_languages() -> list:
        """Return list of supported languages"""
        return list(ReviewerFactory.REVIEWER_MAP.keys())
    
    @staticmethod
    def is_language_supported(language: str) -> bool:
        """Check if language is supported"""
        return language.lower() in ReviewerFactory.REVIEWER_MAP
