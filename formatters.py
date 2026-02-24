"""
Comment formatting for Bitbucket
"""

from datetime import datetime
from typing import Dict, List, Optional


class CommentFormatter:
    """Format AI review as Bitbucket comment"""
    
    @staticmethod
    def format(
        review_content: str,
        pr_details: Dict,
        stats: Dict,
        cost: Optional[float] = None,
        custom_issues: List[Dict] = None,
        confidence_score: Optional[float] = None,
        learning_resources: Optional[List[Dict]] = None,
        similar_code: Optional[List[Dict]] = None
    ) -> str:
        """Format complete review comment"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        model = stats.get('model', 'gpt-4o-mini')
        files = stats.get('files', 0)
        author = pr_details.get('author', {}).get('display_name', 'N/A')
        
        header = f"""## 🤖 AI Code Review by CodeWise

| 📊 **Review Details** | |
|:---|:---|
| **🕐 Reviewed At** | {timestamp} |
| **🧠 AI Model** | {model} |
| **📁 Files Analyzed** | {files} |
| **👤 PR Author** | {author} |
"""
        
        # Add confidence score if available
        if confidence_score is not None:
            confidence_icon = "🟢" if confidence_score >= 0.8 else "🟡" if confidence_score >= 0.6 else "🔴"
            header += f"| **{confidence_icon} Confidence Score** | {confidence_score:.0%} |\n"
        
        header += "\n---\n\n"
        
        # Main review content
        body = review_content
        
        # Add learning resources if available
        if learning_resources:
            body += "\n\n---\n\n### 📚 Learning Resources\n\n"
            body += "*Based on the issues found, these resources might be helpful:*\n\n"
            for resource in learning_resources[:5]:  # Top 5 resources
                body += f"- **{resource['title']}**: {resource['url']}\n"
                if resource.get('description'):
                    body += f"  *{resource['description']}*\n"
                body += "\n"
        
        # Footer
        footer = "\n\n---\n\n"
        if cost:
            footer += f"*🤖 Powered by **CodeWise** • AI Model: {model} • Cost: ~${cost:.4f}*\n\n"
        else:
            footer += f"*🤖 Powered by **CodeWise** • AI Model: {model}*\n\n"
        footer += "*This is an automated code review. Please verify all suggestions before applying.*"
        
        return header + body + footer
