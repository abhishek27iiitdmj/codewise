"""
Diff filtering and processing
"""

import re
from typing import Tuple, Dict, List
from utils import logger


class DiffFilter:
    """Filter and process PR diffs"""
    
    def __init__(self, exclude_patterns: List[str], max_diff_size: int, max_files: int):
        self.exclude_patterns = exclude_patterns
        self.max_diff_size = max_diff_size
        self.max_files = max_files
    
    def should_exclude(self, filepath: str) -> bool:
        """Check if file should be excluded"""
        import fnmatch
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(filepath, pattern):
                return True
        return False
    
    def filter_diff(self, diff_text: str) -> Tuple[str, Dict]:
        """Filter diff and return (filtered_diff, stats)"""
        lines = diff_text.split('\n')
        filtered_lines = []
        current_file = None
        file_count = 0
        excluded_files = []
        changed_files = []
        
        for line in lines:
            if line.startswith('diff --git'):
                # Extract filename
                match = re.search(r'b/(.+)$', line)
                if match:
                    current_file = match.group(1)
                    if self.should_exclude(current_file):
                        excluded_files.append(current_file)
                        current_file = None
                        continue
                    changed_files.append(current_file)
                    file_count += 1
                    if file_count > self.max_files:
                        logger.warning(f"Max files limit ({self.max_files}) reached")
                        break
            
            if current_file is not None:
                filtered_lines.append(line)
        
        filtered_diff = '\n'.join(filtered_lines)
        diff_line_count = len(filtered_lines)
        
        stats = {
            'total_files': file_count,
            'excluded_files': excluded_files,
            'changed_files': changed_files,
            'diff_lines': diff_line_count,
            'exceeds_limit': diff_line_count > self.max_diff_size
        }
        
        return filtered_diff, stats
