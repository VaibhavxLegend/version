# app/services/llm.py
from typing import List, Dict
import re

from ..utils.logging import get_logger
from ..config.settings import settings

logger = get_logger(__name__)


def force_single_line(text: str) -> str:
    """Fast, efficient function to force text to be a single line."""
    if not text:
        return ""
    
    # Convert to string and truncate early if too long to prevent timeout
    text = str(text)[:1000]  # Limit processing to first 1000 chars
    
    # Use regex for efficient bulk replacement
    text = re.sub(r'[\r\n\t\f\v\x0b\x0c]', ' ', text)
    text = text.replace('\\n', ' ').replace('\\r', ' ').replace('\\t', ' ')
    
    # Use regex to collapse spaces efficiently
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Truncate to reasonable length
    if len(text) > 200:
        text = text[:197] + "..."
    
    return text


class GeminiLLM:
    """LLM facade that returns single-line, plain-text answers (no markdown)."""

    def __init__(self) -> None:
        try:
            self.api_key = settings.gemini_api_key.get_secret_value()
        except Exception:
            self.api_key = None

    async def generate_single_line_answer(
        self,
        question: str,
        context_chunks: List[str],
        max_tokens: int = 100,
    ) -> str:
        """Fast generation of single-line answer to prevent worker timeouts."""
        if not context_chunks:
            return "No relevant information found in document."
            
        # Fast processing - limit context size immediately
        limited_chunks = [chunk[:1000] for chunk in context_chunks[:1]]  # Only first chunk, limit size
        
        # Quick extraction
        answer = self._extract_single_line_answer(question, limited_chunks)
        
        # Fast cleanup
        answer = force_single_line(answer)
        
        # Early truncation
        if len(answer) > 100:
            answer = answer[:97] + "..."
            
        logger.info("Generated fast answer")
        return answer

    def _build_single_line_prompt(self, question: str, context_chunks: List[str]) -> str:
        """Create a prompt optimized for single-line, plain-text responses."""
        context_text = " ".join(context_chunks[:3])
        prompt = (
            "Based on the following context, provide a single, concise sentence answer to the question.\n\n"
            f"Context: {context_text[:1000]}...\n\n"
            f"Question: {question}\n\n"
            "Instructions:\n"
            "- Answer in ONE sentence only\n"
            "- Be precise and factual\n"
            "- Include relevant clause/section reference if available\n"
            "- Maximum 25 words\n"
            "- Return PLAIN TEXT ONLY (no markdown and no line breaks)\n\n"
            "Answer:"
        )
        return prompt

    def _extract_single_line_answer(self, question: str, context_chunks: List[str]) -> str:
        """Fast extraction of single-line answer to prevent worker timeouts."""
        if not context_chunks:
            return "No relevant information found in the document."

        # Limit processing to prevent timeouts - take only first chunk and limit size
        context = context_chunks[0][:2000] if context_chunks else ""
        context = force_single_line(context).lower()
        
        question_lower = question.lower()
        
        # Fast keyword search - just find first sentence with question keywords
        question_words = [w for w in question_lower.split() if len(w) > 3][:5]  # Limit words
        
        # Quick sentence split - limit to first 5 sentences only
        sentences = [s.strip() for s in context.split('.')[:5] if len(s.strip()) > 10]
        
        for sentence in sentences:
            if len(sentence) > 300:  # Skip very long sentences to avoid timeout
                continue
                
            # Quick check if sentence contains any question keywords
            if any(word in sentence.lower() for word in question_words):
                result = sentence[:150].strip()  # Truncate early
                if not result.endswith('.'):
                    result += '.'
                return result.capitalize()
        
        # Fast fallback - just return first reasonable sentence
        if sentences:
            result = sentences[0][:100].strip()
            if not result.endswith('.'):
                result += '.'
            return result.capitalize()
        
        return "Information not found in document."

    async def generate_answer(
        self,
        question: str,
        context_chunks: List[str],
        max_tokens: int = 512,
        temperature: float = 0.0,
    ) -> Dict[str, str]:
        """Legacy method for compatibility."""
        answer = await self.generate_single_line_answer(question, context_chunks, 100)
        return {"answers": answer}
