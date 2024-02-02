from difflib import SequenceMatcher


def compute_similarity_score(s1: str, s2: str) -> float:
    s1_lower = s1.lower()
    s2_lower = s2.lower()

    return SequenceMatcher(None, s1_lower, s2_lower).ratio()
