# A Newton-Face and p-Adic Proof of the Two-Dimensional Gaussian Moments Conjecture

Casey Atwell — Independent Researcher

This repository is the public reproducibility companion to the Zenodo publication:

**Zenodo DOI:** [10.5281/zenodo.21611931](https://doi.org/10.5281/zenodo.21611931)

**Zenodo record:** https://zenodo.org/records/21611931

## Status

The manuscript presents a claimed complete proof of the two-dimensional Gaussian Moments Conjecture for independent specialist verification. Publication on Zenodo or GitHub is not represented as independent peer certification.

## Repository structure

- `paper/` — manuscript PDF and TeX source.
- `verification/` — exact-arithmetic verification script and captured transcript.
- `audits/` — reviewer supplement and the integrity manifest of the controlling scientific object.

## Verification

From the repository root, run:

```text
python verification/verify_newton_frobenius.py
```

The supplied scientific-review package specifies Python standard-library execution with seed `20260724` and 39 completed passing trials. Compare the result with `verification/verification_transcript.txt`.

The computation is supporting verification. It does not replace deductive review of the universal theorem.

## Scientific object

The underlying reviewed scientific object is **GMC(2) Scientific Review v0.2**. Its files have been carried into this GitHub staging package without mathematical modification.

## Citation

Please cite the Zenodo archival record using DOI `10.5281/zenodo.21611931`. Machine-readable citation metadata is provided in `CITATION.cff`.

## License

Manuscript and non-software materials are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). Verification software is licensed under the MIT License. See `LICENSE.md`.
