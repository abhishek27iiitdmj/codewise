"""
API clients for Bitbucket and OpenAI
"""

import time
import requests
from typing import Dict, Tuple
from openai import OpenAI
from utils import logger, sanitize_log


class BitbucketClient:
    """Bitbucket API client"""
    
    def __init__(self, workspace: str, repo: str, token: str):
        self.workspace = workspace
        self.repo = repo
        self.token = token
        self.base_url = "https://api.bitbucket.org/2.0"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with retries"""
        url = f"{self.base_url}{endpoint}"
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"API request: {method} {sanitize_log(url)}")
                response = requests.request(method, url, headers=self.headers, timeout=30, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    logger.error(f"Bitbucket API request failed after {max_retries} attempts: {e}")
                    raise
                logger.warning(f"Retry {attempt + 1}/{max_retries} after error: {e}")
                time.sleep(2 ** attempt)
    
    def get_pr_details(self, pr_id: str) -> Dict:
        """Fetch PR metadata"""
        endpoint = f"/repositories/{self.workspace}/{self.repo}/pullrequests/{pr_id}"
        response = self._request("GET", endpoint)
        return response.json()
    
    def get_pr_diff(self, pr_id: str) -> str:
        """Fetch PR diff"""
        endpoint = f"/repositories/{self.workspace}/{self.repo}/pullrequests/{pr_id}/diff"
        response = self._request("GET", endpoint)
        return response.text
    
    def get_file_content(self, filepath: str, branch: str) -> str:
        """Fetch full file content from a specific branch"""
        endpoint = f"/repositories/{self.workspace}/{self.repo}/src/{branch}/{filepath}"
        try:
            response = self._request("GET", endpoint)
            return response.text
        except Exception as e:
            logger.warning(f"Failed to fetch {filepath}: {e}")
            return ""
    
    def post_comment(self, pr_id: str, content: str) -> Dict:
        """Post comment on PR"""
        endpoint = f"/repositories/{self.workspace}/{self.repo}/pullrequests/{pr_id}/comments"
        data = {"content": {"raw": content}}
        response = self._request("POST", endpoint, json=data)
        return response.json()


class OpenAIClient:
    """OpenAI API client"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", temperature: float = 0.2, max_tokens: int = 2000):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def review_code(self, system_prompt: str, user_prompt: str) -> Tuple[str, int, int]:
        """Send code for AI review, returns (response, input_tokens, output_tokens)"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Calling OpenAI API with model {self.model}")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                content = response.choices[0].message.content
                input_tokens = response.usage.prompt_tokens
                output_tokens = response.usage.completion_tokens
                
                logger.info(f"OpenAI API success: {input_tokens} input tokens, {output_tokens} output tokens")
                return content, input_tokens, output_tokens
                
            except Exception as e:
                if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                    wait_time = 2 ** (attempt + 1)
                    logger.warning(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(wait_time)
                elif attempt == max_retries - 1:
                    logger.error(f"OpenAI API failed after {max_retries} attempts: {e}")
                    raise
                else:
                    logger.warning(f"OpenAI API error, retry {attempt + 1}/{max_retries}: {e}")
                    time.sleep(2 ** attempt)
