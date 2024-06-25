import numpy as np
from typing import Dict


def create_walnut53_mapping() -> Dict[str, str]:
    rng = np.random.default_rng(seed=53)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    walnut53_permutation = rng.permutation(len(alphabet))
    return {a: alphabet[b] for a, b in zip(alphabet, walnut53_permutation)}


WALNUT53_MAPPING = create_walnut53_mapping()
WALNUT53_REVERSE = {v: k for k, v in WALNUT53_MAPPING.items()}


def walnut53_encode(text: str) -> str:
    return "|".join(WALNUT53_MAPPING.get(c.lower(), c) for c in text)


def walnut53_decode(text: str) -> str:
    return "".join(WALNUT53_REVERSE.get(c, c) for c in text.split("|"))
