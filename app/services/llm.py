# app/services/llm.py
import requests
import json
import re
from typing import List, Dict, Optional
from ..utils.logging import get_logger
from ..config.settings import settings

logger = get_logger(__name__)

class GeminiLLM:
    def __init__(self):
        # Initialize Gemini LLM client with API key if applicable
        try:
            self.api_key = settings.gemini_api_key.get_secret_value()
        except:
            self.api_key = None
        
    async def generate_single_line_answer(
        self,
        question: str,
        context_chunks: List[str],
        max_tokens: int = 100
    ) -> str:
        """
        Generate a single-line, concise answer from the context.
        """
        # Build optimized prompt for single-line responses
        prompt = self._build_single_line_prompt(question, context_chunks)
        
        # For now, use rule-based extraction since we don't have actual LLM API
        answer = self._extract_single_line_answer(question, context_chunks)
        
        logger.info("Generated single-line answer")
        return answer

    def _build_single_line_prompt(self, question: str, context_chunks: List[str]) -> str:
        """
        Create a prompt specifically optimized for single-line responses.
        """
        context_text = " ".join(context_chunks[:3])  # Limit context for efficiency
        
        prompt = f"""Based on the following context, provide a single, concise sentence answer to the question.
        
Context: {context_text[:1000]}...

Question: {question}

Instructions:
- Answer in ONE sentence only
- Be precise and factual
- Include relevant clause/section reference if available
- Maximum 25 words

Answer:"""
        
        return prompt

    def _extract_single_line_answer(self, question: str, context_chunks: List[str]) -> str:
        """
        Extract a single-line answer from context using rule-based approach.
        """
        if not context_chunks:
            return "No relevant information found in the document."
            
        # Combine all context
        full_context = " ".join(context_chunks).lower()
        question_lower = question.lower()
        
        # Key patterns to look for single-line extractions
        patterns = [
            # Coverage/policy patterns
            r"the company.*?shall.*?(?:indemnify|pay|cover).*?(?:\.|;)",
            r"coverage.*?includes?.*?(?:\.|;)",
            r"benefits.*?(?:are|include).*?(?:\.|;)",
            
            # Definition patterns  
            r"means.*?(?:\.|;)",
            r"defined as.*?(?:\.|;)",
            r"refers to.*?(?:\.|;)",
            
            # Condition patterns
            r"(?:if|when|provided|subject to).*?(?:\.|;)",
            r"eligibility.*?(?:\.|;)",
            r"conditions.*?(?:\.|;)",
        ]
        
        # Find the most relevant single sentence
        for pattern in patterns:
            matches = re.findall(pattern, full_context, re.IGNORECASE | re.DOTALL)
            if matches:
                # Clean and return the first match
                answer = matches[0].strip()
                answer = ' '.join(answer.split())  # Clean whitespace
                
                # Ensure it's reasonably short for single-line
                if len(answer) > 150:
                    answer = answer[:147] + "..."
                    
                # Capitalize first letter
                if answer:
                    answer = answer[0].upper() + answer[1:] if len(answer) > 1 else answer.upper()
                
                return answer
        
        # Fallback: extract key sentence containing question keywords
        question_words = [w for w in question_lower.split() if len(w) > 3]
        sentences = full_context.split('.')
        
        best_sentence = ""
        best_score = 0
        
        for sentence in sentences[:20]:  # Check first 20 sentences
            sentence = sentence.strip()
            if len(sentence) < 20 or len(sentence) > 200:  # Skip too short/long
                continue
                
            score = sum(1 for word in question_words if word in sentence.lower())
            if score > best_score and score > 0:
                best_score = score
                best_sentence = sentence
        
        if best_sentence:
            # Clean and format
            best_sentence = ' '.join(best_sentence.split())
            if best_sentence and not best_sentence.endswith('.'):
                best_sentence += '.'
            return best_sentence[0].upper() + best_sentence[1:] if len(best_sentence) > 1 else best_sentence
        
        return "Relevant information not clearly specified in the provided document."

    async def generate_answer(
        self,
        question: str,
        context_chunks: List[str],
        max_tokens: int = 512,
        temperature: float = 0.0
    ) -> Dict[str, str]:
        """
        Legacy method - now returns single-line answer format.
        """
        single_line = await self.generate_single_line_answer(question, context_chunks, 100)
        return {"answers": single_line}
