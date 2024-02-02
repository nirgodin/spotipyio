from difflib import SequenceMatcher


def compute_similarity_score(s1: str, s2: str) -> float:
    s1_processed = s1.lower().strip()
    s2_processed = s2.lower().strip()

    return SequenceMatcher(None, s1_processed, s2_processed).ratio()
