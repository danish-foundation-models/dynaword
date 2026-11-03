from collections.abc import Set
from string import punctuation

from dacy.resources import load_ods_fullforms

BOUNDARY_PUNCTUATION = punctuation + "…“”„‘’«»–—"


def danish_vocabulary() -> set[str]:
    """Load case-folded Danish ODS word forms using DaCy."""
    return {word.casefold() for word in load_ods_fullforms()["form"]}


def vocabulary_coverage(text: str, vocabulary: Set[str]) -> float:
    """Compare the text's words with a vocabulary and return a score from 0 to 1."""
    words = {
        word.strip(BOUNDARY_PUNCTUATION)
        for word in text.casefold().split()
        if any(char.isalpha() for char in word)
    }
    return len(words & vocabulary) / len(words) if words else 0.0
