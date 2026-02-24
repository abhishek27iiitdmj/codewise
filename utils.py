"""
Utility functions for AI Code Review Bot
"""

import logging
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def sanitize_log(message: str) -> str:
    """Sanitize log messages to redact API keys and tokens"""
    message = re.sub(r'(sk-[a-zA-Z0-9]{20,})', '[REDACTED_OPENAI_KEY]', message)
    message = re.sub(r'(ATB[a-zA-Z0-9]{20,})', '[REDACTED_BB_TOKEN]', message)
    message = re.sub(r'(Bearer\s+[a-zA-Z0-9\-_]+)', 'Bearer [REDACTED]', message)
    return message


def calculate_cost(input_tokens: int, output_tokens: int, model: str = "gpt-4o-mini") -> float:
    """Calculate OpenAI API cost"""
    if "gpt-4o" in model or "gpt-4-turbo" in model:
        if "mini" in model:
            input_cost = 0.00015 / 1000
            output_cost = 0.0006 / 1000
        else:
            input_cost = 0.0025 / 1000
            output_cost = 0.01 / 1000
    elif "gpt-4" in model:
        input_cost = 0.03 / 1000
        output_cost = 0.06 / 1000
    else:  # gpt-3.5-turbo
        input_cost = 0.0015 / 1000
        output_cost = 0.002 / 1000
    
    return (input_tokens * input_cost) + (output_tokens * output_cost)
