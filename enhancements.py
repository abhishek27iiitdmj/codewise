"""
Enhanced features for AI Code Review Bot
- Multi-File Context Retrieval
- Confidence Scoring
- Learning Resources
- Codebase Similarity Search
"""

import os
import re
from typing import Dict, List, Optional
from utils import logger


class MultiFileContext:
    """Retrieve full file contents for better context"""
    
    def __init__(self, bb_client, max_files: int = 5, max_file_size: int = 10000):
        self.bb_client = bb_client
        self.max_files = max_files
        self.max_file_size = max_file_size
    
    def get_full_files(self, changed_files: List[str], branch: str) -> Dict[str, str]:
        """Fetch full content of changed files"""
        full_files = {}
        
        for i, filepath in enumerate(changed_files[:self.max_files]):
            if i >= self.max_files:
                logger.info(f"Reached max files limit ({self.max_files}) for context retrieval")
                break
            
            try:
                logger.debug(f"Fetching full content of {filepath}")
                content = self.bb_client.get_file_content(filepath, branch)
                
                if content and len(content) <= self.max_file_size:
                    full_files[filepath] = content
                    logger.info(f"Retrieved {filepath} ({len(content)} chars)")
                elif len(content) > self.max_file_size:
                    # Truncate large files
                    full_files[filepath] = content[:self.max_file_size] + "\n\n// ... (truncated)"
                    logger.info(f"Retrieved {filepath} (truncated from {len(content)} to {self.max_file_size} chars)")
            except Exception as e:
                logger.warning(f"Failed to retrieve {filepath}: {e}")
        
        return full_files


class ConfidenceScorer:
    """Analyze AI review confidence based on response patterns"""
    
    @staticmethod
    def calculate_confidence(review_content: str) -> float:
        """
        Calculate confidence score (0.0 to 1.0) based on:
        - Presence of uncertainty phrases
        - Specificity of recommendations
        - Number of code examples provided
        """
        confidence_score = 1.0
        
        # Uncertainty phrases reduce confidence
        uncertainty_patterns = [
            r'\bmight\b', r'\bmay\b', r'\bpossibly\b', r'\bperhaps\b',
            r'\buncertain\b', r'\bnot sure\b', r'\bseems like\b',
            r'\bcould be\b', r'\bappears to\b'
        ]
        
        uncertainty_count = sum(
            len(re.findall(pattern, review_content, re.IGNORECASE))
            for pattern in uncertainty_patterns
        )
        
        # Each uncertainty phrase reduces confidence by 5%
        confidence_score -= min(uncertainty_count * 0.05, 0.3)
        
        # Code examples increase confidence
        code_blocks = len(re.findall(r'```\w+\n', review_content))
        confidence_score += min(code_blocks * 0.05, 0.15)
        
        # Specific line references increase confidence
        line_refs = len(re.findall(r'line\s+\d+', review_content, re.IGNORECASE))
        confidence_score += min(line_refs * 0.02, 0.1)
        
        # File references increase confidence
        file_refs = len(re.findall(r'\b[\w/]+\.php\b', review_content))
        confidence_score += min(file_refs * 0.02, 0.1)
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, confidence_score))


class SimilaritySearch:
    """Find similar code patterns in the codebase"""
    
    def __init__(self, workspace_root: str = '.'):
        self.workspace_root = workspace_root
    
    def extract_code_signature(self, code: str) -> str:
        """Extract code signature for matching (simplified approach)"""
        # Remove comments, whitespace, normalize
        signature = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        signature = re.sub(r'/\*.*?\*/', '', signature, flags=re.DOTALL)
        signature = re.sub(r'\s+', ' ', signature)
        signature = signature.strip().lower()
        return signature
    
    def find_similar_code(self, changed_files: List[str], max_results: int = 5) -> List[Dict]:
        """Find similar code patterns in the codebase"""
        return []  # Placeholder for similarity search
