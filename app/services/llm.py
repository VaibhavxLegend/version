# app/services/llm.py
from typing import List, Dict
import re

from ..utils.logging import get_logger
from ..config.settings import settings

logger = get_logger(__name__)


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
        """Generate a concise, single-line, plain-text answer from context."""
        # Prompt kept for potential future LLM integration
        _ = self._build_single_line_prompt(question, context_chunks)

        # Rule-based extraction for now
        answer = self._extract_single_line_answer(question, context_chunks)

        # Enforce plain-text single line
        answer = self._strip_markdown(answer)
        # ULTRA-aggressive final safeguard: ensure no newlines remain
        answer = answer.replace("\\n", " ").replace("\\r", " ").replace("\\t", " ")
        answer = answer.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        answer = re.sub(r"[\r\n\t\f\v\x0b\x0c]+", " ", answer)  # All line breaks and form feeds
        answer = re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", answer)   # Remove control characters
        answer = " ".join(answer.split())  # Normalize all whitespace to single spaces
        logger.info("Generated single-line answer")
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
        """Extract a single-line answer from context using simple rules."""
        if not context_chunks:
            return "No relevant information found in the document."

        full_context = " ".join(context_chunks).lower()
        question_lower = question.lower()

        # Target common policy/definition/condition statements
        patterns = [
            r"the company.*?shall.*?(?:indemnify|pay|cover).*?(?:\.|;)",  # Indemnity and payment obligations
            r"coverage.*?includes?.*?(?:\.|;)",                        # Coverage inclusions
            r"benefits.*?(?:are|include).*?(?:\.|;)",                 # Benefits description
            r"means.*?(?:\.|;)",                                      # Definition of terms
            r"defined as.*?(?:\.|;)",                                 # Terms defined as
            r"refers to.*?(?:\.|;)",                                  # References to terms
            r"(?:if|when|provided|subject to).*?(?:\.|;)",           # Conditional clauses
            r"eligibility.*?(?:\.|;)",                                # Eligibility criteria
            r"conditions.*?(?:\.|;)",                                 # Conditions precedent
        ]

        for pattern in patterns:
            matches = re.findall(pattern, full_context, re.IGNORECASE | re.DOTALL)
            if matches:
                ans = " ".join(matches[0].strip().split())
                # Remove all newline variations from extracted answer
                ans = ans.replace("\\n", " ").replace("\\r", " ").replace("\n", " ").replace("\r", " ")
                ans = " ".join(ans.split())  # Normalize whitespace
                if len(ans) > 150:
                    ans = ans[:147] + "..."
                return ans[0].upper() + ans[1:] if len(ans) > 1 else ans.upper()

        # Fallback: best overlapping sentence with question keywords
        question_words = [w for w in question_lower.split() if len(w) > 3]
        sentences = full_context.split(".")
        best_sentence = ""
        best_score = 0
        for sentence in sentences[:20]:
            s = sentence.strip()
            if 20 <= len(s) <= 200:
                score = sum(1 for w in question_words if w in s)
                if score > best_score and score > 0:
                    best_score = score
                    best_sentence = s

        if best_sentence:
            if not best_sentence.endswith("."):
                best_sentence += "."
            # Remove all newline variations from best sentence
            best_sentence = best_sentence.replace("\\n", " ").replace("\\r", " ").replace("\n", " ").replace("\r", " ")
            best_sentence = " ".join(best_sentence.split())
            return best_sentence[0].upper() + best_sentence[1:] if len(best_sentence) > 1 else best_sentence

        return "Relevant information not clearly specified in the provided document."

    def _strip_markdown(self, text: str) -> str:
        """Remove markdown and newlines; collapse whitespace to a single line."""
        if not text:
            return ""
        # Remove fenced code blocks and inline code
        text = re.sub(r"```[\s\S]*?```", " ", text)
        text = re.sub(r"`+([^`]+)`+", r"\1", text)
        # Images -> alt text; Links -> link text
        text = re.sub(r"!\[([^\]]*)\]\([^\)]*\)", r"\1", text)
        text = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", text)
        # Headings, blockquotes, lists, emphasis
        text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s{0,3}>\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", text)
        # Remove leftover markdown-y punctuation
        text = text.replace("#", " ").replace("*", " ").replace("`", " ")
        # AGGRESSIVE newline removal - handle all possible variations
        text = text.replace("\\n", " ").replace("\\r", " ").replace("\\t", " ")
        text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        text = re.sub(r"[\r\n\t\f\v]+", " ", text)  # All whitespace chars
        text = re.sub(r"\s+", " ", text).strip()
        # Remove any remaining control characters
        text = re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:300]

    async def generate_answer(
        self,
        question: str,
        context_chunks: List[str],
        max_tokens: int = 512,
        temperature: float = 0.0,
    ) -> Dict[str, str]:
        """Legacy method; returns a plain-text single-line answer in {"answers": str}."""
        single_line = await self.generate_single_line_answer(question, context_chunks, 100)
        single_line = self._strip_markdown(single_line)
        return {"answers": single_line}
