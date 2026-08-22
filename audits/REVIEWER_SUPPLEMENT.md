# Reviewer Supplement

## A Newton-Face and p-Adic Proof of the Two-Dimensional Gaussian Moments Conjecture

**Casey Atwell**  
**Scientific-review package v0.2**  
**July 24, 2026**

This supplement is not part of the mathematical proof. It records the exact computational audit, identifies the load-bearing proof transitions, and provides reproducibility metadata for reviewers.

## 1. Claim status

The accompanying preprint presents a complete proof of the two-dimensional Gaussian Moments Conjecture. The argument has survived repeated internal audits and the exact-integer stress test described below. It has not yet received independent specialist acceptance.

The appropriate review status is:

> High-confidence complete proof candidate, not yet independently certified.

The computational results are supporting evidence only. They do not establish the theorem's universal quantifiers.

## 2. Exact-integer stress test

The script `verify_newton_frobenius.py` independently tests the proof's finite connective mechanism on generated polynomials.

For every completed trial it:

1. generates a polynomial in two complex Gaussian variables with weight support meeting both sides of zero;
2. constructs the lowest supporting face of the transformed support;
3. searches for a power `N` with nonzero face constant term;
4. verifies that `J = N beta` is integral;
5. expands `R = P-hat^N` exactly;
6. confirms that no diagonal coefficient occurs below `J`;
7. selects a prime `p > J` for which the distinguished coefficient is nonzero modulo `p`;
8. expands `R^p` exactly;
9. verifies the Frobenius coefficient congruences;
10. computes every relevant factorial valuation;
11. verifies that the term at `L = pJ` is the unique minimum-valuation summand;
12. directly evaluates the factorially weighted diagonal moment and confirms that it is nonzero.

### Publication run

- Seed: `20260724`
- Completed trials: `39`
- Attempts: `39`
- Skipped trials: `0`
- Degree bound in each of `Z,W`: `3`
- Number of nonzero terms: between `3` and `5`
- Coefficient set: `{-2,-1,1,2}`
- Maximum searched face power: `8`
- Prime search bound: `31`
- Arithmetic: exact Python integers and rational numbers
- External symbolic or numerical libraries: none
- Result: `39/39 PASS`

The complete output is preserved in `verification_transcript.txt`.

## 3. What the test does and does not establish

The test directly verifies, for each generated case:

- the lower-face support inequality;
- strict isolation of the lowest diagonal height;
- integrality of `J`;
- the Frobenius congruence at the distinguished coefficient;
- divisibility of all coefficients in the interval immediately above it;
- the unique-minimum factorial valuation;
- nonvanishing of the resulting moment.

It does not verify:

- the Duistermaat-van der Kallen theorem;
- the algebraic-specialization lemma over arbitrary complex coefficients;
- existence of suitable unramified primes in a general number field;
- the universal theorem by exhaustive enumeration.

Those points remain deductive dependencies of the manuscript.

## 4. Load-bearing transitions for review

Reviewers are especially invited to inspect the following.

### A. Lowest supporting face

From zero lying in the projected weight convex hull, does the minimization at first coordinate zero produce a finite supporting line

`h >= alpha k + beta`

whose equality face still has zero in the convex hull of its weights?

### B. Constant-term theorem

Is the Duistermaat-van der Kallen theorem used in exactly the following contrapositive form?

`0 in Newt(F)  =>  CT(F^N) != 0 for some N >= 1.`

### C. Algebraic specialization

Does the localization

`(Q[C_1,...,C_r]/I)_B`

preserve simultaneously:

- all moment equations;
- every support coefficient as nonzero;
- the selected face coefficient as nonzero?

### D. Frobenius interval

For

`pJ < L < p(J+1)`,

is it correct that `L` is not divisible by `p`, so the Frobenius sum contains no monomial of `u`-degree `L` and the coefficient `d_L` lies in the selected prime ideal?

### E. Unique minimum valuation

Is

`d_{pJ}(pJ)!`

the unique summand of valuation `J`, including when `J=0`?

A counterexample to any one of these transitions invalidates the proof and should be reported directly.

## 5. Backward dependency chain

The contradiction can be audited backward as follows.

To prove

`E[P^(Np)] != 0`,

it is enough to show that one term in

`Lambda(R^p) = sum_L d_L L!`

has uniquely minimal prime-ideal valuation.

This follows if:

- `d_{pJ}` is a unit;
- every `d_L` for `pJ < L < p(J+1)` lies in the prime ideal;
- no diagonal coefficient occurs below `pJ`;
- factorial valuations are `J` below `p(J+1)` and at least `J+1` thereafter.

The coefficient conditions follow from Frobenius and the support inequality for `R`. The support inequality and nonzero coefficient at `(0,J)` follow from the lowest Newton face and the nonzero constant term in a power of its face polynomial. The algebraic-specialization lemma allows reduction modulo prime ideals while preserving all moment equations and the selected coefficient.

The dependency order is therefore:

`P -> support -> lowest face -> N -> A,J -> algebraic specialization -> prime p -> Frobenius separation -> valuation isolation -> nonzero moment.`

In particular, `N` and `J` are fixed before the prime is chosen.

## 6. Reproducibility files

The scientific-review package contains:

- `GMC2_Preprint_v0_2.pdf`
- `GMC2_Preprint_v0_2.tex`
- `REVIEWER_SUPPLEMENT.md`
- `verify_newton_frobenius.py`
- `verification_transcript.txt`
- `README.md`
- `SHA256SUMS.txt`

The integrity manifest should be checked before review.
