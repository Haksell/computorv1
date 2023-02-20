from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
import re

from utils import ft_assert

LEGIT_CHARACTERS = "0123456789X=.-+*^"
REGEX_A = r"(?:[+-])(?:\d+)(?:\.\d+)?"
REGEX_P = r"X(?:\^\d+)?"
REGEX_MONOMIAL = rf"({REGEX_A})\*({REGEX_P})|({REGEX_A})|({REGEX_P})"
REGEX_POLYNOMIAL = rf"({REGEX_MONOMIAL})+"


@dataclass
class Monomial:
    a: Decimal
    p: int


def create_monomial(a1, p1, a2, p2):
    a = Decimal(1 if p2 else a1 if a1 else a2)
    p = p1 or p2
    p = 0 if p == "" else 1 if p == "X" else int(p[2:])
    return Monomial(a, p)


def reduce_equation(left, right):
    reduced = defaultdict(Decimal)
    for monomial in left:
        reduced[monomial.p] += monomial.a
    for monomial in right:
        reduced[monomial.p] -= monomial.a
    return {p: a for p, a in reduced.items() if a != 0}


def parse_polynomial(s):
    if s[0].isdigit():
        s = "+" + s
    ft_assert(re.fullmatch(REGEX_POLYNOMIAL, s), f'"{s}" is not properly formatted')
    polynomial = re.findall(REGEX_MONOMIAL, s)
    return [create_monomial(*groups) for groups in polynomial]


def parse_equation(s):
    s = "".join(c for c in s if not c.isspace())
    ft_assert(s.count("=") == 1, "There should be exactly one equal sign")
    ft_assert(
        all(c in LEGIT_CHARACTERS for c in s), "Unknown character present in string"
    )
    left, right = s.split("=")
    assert left and right
    left, right = parse_polynomial(left), parse_polynomial(right)
    return reduce_equation(left, right)