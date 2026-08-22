#!/usr/bin/env python3
r"""Exact-integer stress test for the Newton-face/Frobenius mechanism.

This script is supplementary evidence only. It does not prove the theorem.
It generates small two-variable polynomials P(Z,W) with integer coefficients,
requires their weight support to meet both sides of zero, constructs the lowest
supporting face of \hat P(s,u)=P(s,u/s), finds a power with nonzero face
constant term, and verifies the full finite p-adic isolation mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial
import random
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Point = Tuple[int, int]       # (weight k, height h)
Poly2 = Dict[Point, int]      # Laurent in s, ordinary in u
Poly1 = Dict[int, int]        # Laurent in s

SEED = 20260724
TARGET_COMPLETED = 39
MAX_ATTEMPTS = 500
MAX_FACE_POWER = 8
PRIME_BOUND = 31
COEFF_CHOICES = (-2, -1, 1, 2)
DEGREE_BOUND = 3
TERM_MIN = 3
TERM_MAX = 5


def add_term(poly: Dict, key, value: int) -> None:
    if value == 0:
        return
    poly[key] = poly.get(key, 0) + value
    if poly[key] == 0:
        del poly[key]


def mul2(a: Poly2, b: Poly2) -> Poly2:
    out: Poly2 = {}
    for (k1, h1), c1 in a.items():
        for (k2, h2), c2 in b.items():
            add_term(out, (k1 + k2, h1 + h2), c1 * c2)
    return out


def pow2(a: Poly2, n: int) -> Poly2:
    out: Poly2 = {(0, 0): 1}
    base = dict(a)
    e = n
    while e:
        if e & 1:
            out = mul2(out, base)
        e >>= 1
        if e:
            base = mul2(base, base)
    return out


def mul1(a: Poly1, b: Poly1) -> Poly1:
    out: Poly1 = {}
    for k1, c1 in a.items():
        for k2, c2 in b.items():
            add_term(out, k1 + k2, c1 * c2)
    return out


def pow1(a: Poly1, n: int) -> Poly1:
    out: Poly1 = {0: 1}
    base = dict(a)
    e = n
    while e:
        if e & 1:
            out = mul1(out, base)
        e >>= 1
        if e:
            base = mul1(base, base)
    return out


def lower_hull(points: Sequence[Point]) -> List[Point]:
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts

    def cross(o: Point, a: Point, b: Point) -> int:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: List[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    return lower


def lowest_face(points: Sequence[Point]) -> Optional[Tuple[Fraction, Fraction, List[Point]]]:
    """Return (alpha,beta,face) for h >= alpha*k + beta and 0 in face weights."""
    hull = lower_hull(points)
    if not hull:
        return None
    if min(k for k, _ in points) > 0 or max(k for k, _ in points) < 0:
        return None

    # Edge crossing k=0.
    for p, q in zip(hull, hull[1:]):
        k1, h1 = p
        k2, h2 = q
        if k1 <= 0 <= k2 and k1 != k2:
            alpha = Fraction(h2 - h1, k2 - k1)
            beta = Fraction(h1) - alpha * k1
            face = [pt for pt in points if Fraction(pt[1]) == alpha * pt[0] + beta]
            if min(k for k, _ in face) <= 0 <= max(k for k, _ in face):
                return alpha, beta, sorted(face)

    # Vertex at k=0. Choose a finite supporting slope between adjacent lower-hull slopes.
    for i, (k, h) in enumerate(hull):
        if k != 0:
            continue
        left_slope: Optional[Fraction] = None
        right_slope: Optional[Fraction] = None
        if i > 0:
            kl, hl = hull[i - 1]
            left_slope = Fraction(h - hl, k - kl)
        if i + 1 < len(hull):
            kr, hr = hull[i + 1]
            right_slope = Fraction(hr - h, kr - k)
        if left_slope is not None and right_slope is not None:
            alpha = (left_slope + right_slope) / 2
        elif left_slope is not None:
            alpha = left_slope + 1
        elif right_slope is not None:
            alpha = right_slope - 1
        else:
            alpha = Fraction(0)
        beta = Fraction(h)
        if all(Fraction(hh) >= alpha * kk + beta for kk, hh in points):
            face = [pt for pt in points if Fraction(pt[1]) == alpha * pt[0] + beta]
            return alpha, beta, sorted(face)
    return None


def primes_up_to(n: int) -> List[int]:
    out = []
    for x in range(2, n + 1):
        if all(x % d for d in range(2, int(x ** 0.5) + 1)):
            out.append(x)
    return out


def vp(n: int, p: int) -> int:
    if n == 0:
        return 10**9
    n = abs(n)
    v = 0
    while n % p == 0:
        v += 1
        n //= p
    return v


def factorial_vp(n: int, p: int) -> int:
    v = 0
    q = p
    while q <= n:
        v += n // q
        q *= p
    return v


def lambda_value(poly: Poly2) -> int:
    return sum(c * factorial(h) for (k, h), c in poly.items() if k == 0)


def random_polynomial(rng: random.Random) -> Poly2:
    monomials = [(a, b) for a in range(DEGREE_BOUND + 1) for b in range(DEGREE_BOUND + 1) if a + b > 0]
    while True:
        count = rng.randint(TERM_MIN, TERM_MAX)
        chosen = rng.sample(monomials, count)
        weights = [a - b for a, b in chosen]
        if min(weights) <= 0 <= max(weights) and min(weights) < max(weights):
            poly: Poly2 = {}
            for a, b in chosen:
                poly[(a - b, b)] = rng.choice(COEFF_CHOICES)
            return poly


@dataclass
class TrialResult:
    support: List[Tuple[int, int, int]]
    alpha: Fraction
    beta: Fraction
    face: List[Point]
    N: int
    J: int
    A: int
    p: int
    moment: int
    target_valuation: int
    next_valuation: int


def run_trial(P: Poly2) -> Optional[TrialResult]:
    lf = lowest_face(list(P))
    if lf is None:
        return None
    alpha, beta, face = lf

    F: Poly1 = {k: P[(k, h)] for (k, h) in face}
    N = 0
    A = 0
    for n in range(1, MAX_FACE_POWER + 1):
        A = pow1(F, n).get(0, 0)
        if A != 0:
            N = n
            break
    if N == 0:
        return None

    Jq = N * beta
    if Jq.denominator != 1:
        raise AssertionError(f"J not integral: N={N}, beta={beta}")
    J = int(Jq)

    R = pow2(P, N)
    diag = {h: c for (k, h), c in R.items() if k == 0}
    if any(h < J and c != 0 for h, c in diag.items()):
        raise AssertionError("diagonal coefficient below J")
    if diag.get(J, 0) != A:
        raise AssertionError(f"lowest diagonal mismatch: {diag.get(J, 0)} != {A}")
    if any(Fraction(h) < alpha * k + J for (k, h) in R):
        raise AssertionError("supporting inequality failed for R")

    p = 0
    for candidate in primes_up_to(PRIME_BOUND):
        if candidate > J and A % candidate != 0:
            p = candidate
            break
    if p == 0:
        return None

    Rp = pow2(R, p)
    d = {h: c for (k, h), c in Rp.items() if k == 0}
    if any(h < p * J and c != 0 for h, c in d.items()):
        raise AssertionError("R^p has diagonal below pJ")
    if d.get(p * J, 0) % p != pow(A, p, p):
        raise AssertionError("Frobenius target congruence failed")
    if d.get(p * J, 0) % p == 0:
        raise AssertionError("target coefficient divisible by p")
    for L in range(p * J + 1, p * (J + 1)):
        if d.get(L, 0) % p != 0:
            raise AssertionError(f"intermediate coefficient not divisible by p: L={L}")

    summand_vals: List[Tuple[int, int]] = []
    for L, coeff in d.items():
        if coeff == 0:
            continue
        summand_vals.append((L, vp(coeff, p) + factorial_vp(L, p)))
    target_val = dict(summand_vals)[p * J]
    other_vals = [v for L, v in summand_vals if L != p * J]
    if target_val != J:
        raise AssertionError(f"target valuation {target_val}, expected {J}")
    if other_vals and min(other_vals) <= J:
        raise AssertionError("target valuation is not uniquely minimal")

    moment = lambda_value(Rp)
    if moment == 0:
        raise AssertionError("direct factorial moment vanished")
    if vp(moment, p) != J:
        raise AssertionError("sum valuation does not equal unique minimum")

    support = sorted((k, h, c) for (k, h), c in P.items())
    return TrialResult(
        support=support,
        alpha=alpha,
        beta=beta,
        face=face,
        N=N,
        J=J,
        A=A,
        p=p,
        moment=moment,
        target_valuation=target_val,
        next_valuation=min(other_vals) if other_vals else 10**9,
    )


def main() -> None:
    rng = random.Random(SEED)
    completed: List[TrialResult] = []
    skipped = 0
    attempts = 0
    while len(completed) < TARGET_COMPLETED and attempts < MAX_ATTEMPTS:
        attempts += 1
        P = random_polynomial(rng)
        result = run_trial(P)
        if result is None:
            skipped += 1
            continue
        completed.append(result)
        print(
            f"PASS {len(completed):02d}: support={result.support}; "
            f"face={result.face}; alpha={result.alpha}; beta={result.beta}; "
            f"N={result.N}; J={result.J}; A={result.A}; p={result.p}; "
            f"v_target={result.target_valuation}; v_next={result.next_valuation}; "
            f"moment={result.moment}"
        )

    if len(completed) != TARGET_COMPLETED:
        raise SystemExit(
            f"Only {len(completed)} completed trials after {attempts} attempts; skipped={skipped}"
        )

    print("\nSUMMARY")
    print(f"seed={SEED}")
    print(f"completed={len(completed)}")
    print(f"attempts={attempts}")
    print(f"skipped={skipped}")
    print(f"max_face_power={MAX_FACE_POWER}")
    print(f"prime_bound={PRIME_BOUND}")
    print(f"degree_bound={DEGREE_BOUND}")
    print(f"term_count=[{TERM_MIN},{TERM_MAX}]")
    print(f"coefficient_choices={COEFF_CHOICES}")
    print("result=PASS")


if __name__ == "__main__":
    main()
