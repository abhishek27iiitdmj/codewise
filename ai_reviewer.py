#!/usr/bin/env python3
"""
AI Code Review Bot for Bitbucket Pipelines - Multi-Language Support
Automated code review using OpenAI GPT models
Supports: PHP/Laravel, JavaScript/React/Angular/Node, Python/Django/Flask/FastAPI
Enhanced v2.0 with Multi-File Context, Confidence Scoring, Learning Resources, and Similarity Search
"""

import os
import sys
import re
from typing import Dict, List, Tuple

# Import all modules
from config import Config
from clients import BitbucketClient, OpenAIClient
from filters import DiffFilter
from formatters import CommentFormatter
from utils import logger, calculate_cost
from enhancements import (
    MultiFileContext,
    ConfidenceScorer,
    SimilaritySearch
)
from language_detector import LanguageDetector
from reviewer_factory import ReviewerFactory


def parse_pr_url(pr_url: str) -> Tuple[str, str, str]:
    """
    Parse Bitbucket PR URL to extract workspace, repo, and PR ID
    
    Supports formats:
    - https://bitbucket.org/{workspace}/{repo}/pull-requests/{pr_id}
    - https://bitbucket.org/{workspace}/{repo}/pull-requests/{pr_id}/diff
    """
    pattern = r'bitbucket\.org/([^/]+)/([^/]+)/pull-requests/(\d+)'
    match = re.search(pattern, pr_url)
    
    if not match:
        raise ValueError(f"Invalid Bitbucket PR URL format: {pr_url}")
    
    workspace, repo, pr_id = match.groups()
    logger.info(f"Parsed PR URL: workspace={workspace}, repo={repo}, pr_id={pr_id}")
    return workspace, repo, pr_id


def main():
    """Main execution flow with multi-language support"""
    logger.info("Starting AI Code Review Bot v2.0 (Multi-Language)")
    
    # Load configuration
    config = Config()
    
    # Get environment variables
    pr_url = os.getenv('BITBUCKET_PR_URL')
    bb_token = os.getenv('BITBUCKET_APP_PASSWORD')
    openai_key = os.getenv('OPENAI_KEY')
    
    # Parse PR URL if provided (new simplified method)
    if pr_url:
        try:
            workspace, repo, pr_id = parse_pr_url(pr_url)
        except ValueError as e:
            logger.error(str(e))
            sys.exit(1)
    else:
        # Fallback to separate env vars (backward compatibility)
        workspace = os.getenv('BITBUCKET_WORKSPACE')
        repo = os.getenv('BITBUCKET_REPO_SLUG')
        pr_id = os.getenv('BITBUCKET_PR_ID')
    
    # Validate required variables
    if not all([workspace, repo, pr_id, bb_token, openai_key]):
        logger.error("Missing required environment variables")
        logger.error("\nOption 1 (Simplified):")
        logger.error("  - BITBUCKET_PR_URL (e.g., https://bitbucket.org/workspace/repo/pull-requests/123)")
        logger.error("  - BITBUCKET_APP_PASSWORD")
        logger.error("  - OPENAI_KEY")
        logger.error("\nOption 2 (Legacy):")
        logger.error("  - BITBUCKET_WORKSPACE, BITBUCKET_REPO_SLUG, BITBUCKET_PR_ID")
        logger.error("  - BITBUCKET_APP_PASSWORD")
        logger.error("  - OPENAI_KEY")
        sys.exit(1)
    
    logger.info(f"Reviewing PR #{pr_id} in {workspace}/{repo}")
    
    try:
        # Initialize clients
        bb_client = BitbucketClient(workspace, repo, bb_token)
        ai_client = OpenAIClient(
            openai_key,
            model=config.get('model', 'gpt-3.5-turbo'),
            temperature=config.get('temperature', 0.2),
            max_tokens=config.get('max_tokens', 2000)
        )
        
        # Fetch PR details and diff
        logger.info("Fetching PR details...")
        pr_details = bb_client.get_pr_details(pr_id)
        
        logger.info("Fetching PR diff...")
        raw_diff = bb_client.get_pr_diff(pr_id)
        
        # Filter diff
        logger.info("Filtering diff...")
        diff_filter = DiffFilter(
            config.get('exclude_patterns', []),
            config.get('max_diff_size', 5000),
            config.get('max_files', 50)
        )
        filtered_diff, diff_stats = diff_filter.filter_diff(raw_diff)
        
        # Check if PR is too large
        if diff_stats['exceeds_limit'] and config.get('skip_large_prs', True):
            if config.get('post_warning_on_skip', True):
                warning = f"""## ⚠️ AI Code Review Skipped
This pull request is too large for automated AI review.
**Diff size:** {diff_stats['diff_lines']} lines (limit: {config.get('max_diff_size', 5000)})
**Files changed:** {diff_stats['total_files']}
*AI code review works best with focused PRs under 1000 lines of changes.*"""
                bb_client.post_comment(pr_id, warning)
                logger.warning("PR exceeds size limits, review skipped")
            sys.exit(0)
        
        logger.info(f"Diff stats: {diff_stats['total_files']} files, {diff_stats['diff_lines']} lines")
        
        # LANGUAGE DETECTION - Detect programming language from changed files
        logger.info("Detecting programming language...")
        language, framework, lang_stats = LanguageDetector.detect_from_diff(
            filtered_diff, 
            diff_stats.get('changed_files', [])
        )
        language_name = LanguageDetector.get_language_name(language, framework)
        logger.info(f"Detected language: {language_name}")
        
        # Check if language is supported
        if not ReviewerFactory.is_language_supported(language):
            supported = ', '.join(ReviewerFactory.get_supported_languages())
            warning = f"""## ⚠️ Language Not Supported
The detected language **{language}** is not currently supported for automated review.

**Supported languages:** {supported}

**Language distribution in this PR:**
{chr(10).join([f'- {lang}: {count} files' for lang, count in lang_stats.get('language_distribution', {}).items()])}

*Please ensure the PR contains code in one of the supported languages.*"""
            bb_client.post_comment(pr_id, warning)
            logger.warning(f"Language {language} not supported")
            sys.exit(0)
        
        logger.info(f"✅ AI code review completed successfully ({language_name}, v2.0)")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"❌ AI code review failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
