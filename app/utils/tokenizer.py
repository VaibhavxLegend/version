# app/utils/tokenizer.py

from typing import Union

# Example 2: Using HuggingFace tokenizer for other models (e.g., Gemini or Llama)
def count_tokens_transformers(
    text: str,
    tokenizer_obj
) -> int:
    """
    Count tokens using a HuggingFace `PreTrainedTokenizer` instance.
    """
    enc = tokenizer_obj.encode(text)
    return len(enc)

# Example: Simple fallback (not accurate, but prevents crash)
def count_words(text: str) -> int:
    return len(text.split())

