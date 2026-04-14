# RezPie

RezPie is a small numerical-analysis project about approximating `pi` with
classical polygon bounds and simple extrapolation.

The focus is not on beating state-of-the-art high-precision algorithms.
The focus is on understanding convergence:

- how inscribed and circumscribed polygons bound `pi`
- how fast those bounds tighten
- whether extrapolation can improve a basic polygon estimate
- whether perimeter and area approximations can be combined to cancel leading error terms

## What this repo does

For a unit circle, a regular polygon gives perimeter-based approximations to `pi`:

- the inscribed polygon gives a lower bound
- the circumscribed polygon gives an upper bound

Starting from a hexagon, the code repeatedly doubles the number of sides using
half-angle recurrences. From those bounds it computes:

- `lower`: rigorous lower bound
- `upper`: rigorous upper bound
- `mid`: midpoint estimate
- `R2`: Richardson-style extrapolated estimate assuming leading error behaves like `1/n^2`
- `R4`: a diagnostic higher-order probe included mainly to show that not every extrapolation choice helps
- geometry-first perimeter/area blends, including the derived `alpha = 2/3` blend

## What this repo does not claim

This project does **not** claim:

- a new best way to compute `pi`
- a method that beats Chudnovsky
- a replacement for serious arbitrary-precision libraries

Chudnovsky is included as a reference implementation because it is the right
kind of baseline for high-precision comparison.

## Project files

- `rezpie.py`
  Polygon bounds, extrapolation helpers, and convergence utilities.

- `benchmark.py`
  Prints convergence tables for midpoint and extrapolated estimates, and compares
  them against a Chudnovsky implementation.

- `plot_extrapolation.py`
  Plots approximation error and bound width as polygon size increases.

- `chudnovsky.py`
  A direct Chudnovsky implementation used as a serious reference method.

- `geometry_pi.py`
  Geometry-first perimeter and area families, plus blending and extrapolation helpers.

- `benchmark_geometry.py`
  Compares perimeter midpoint, area midpoint, the derived `2/3` blend, and `R4` on that blend.

## Mathematical idea

If a sequence of approximations behaves like

`A_n = pi + c / n^p + ...`

then Richardson extrapolation combines `A_n` and `A_2n` to cancel the leading
error term:

`E_n = (2^p A_2n - A_n) / (2^p - 1)`

This repo tests that idea on polygon-based approximations.

The main question is not "is this the best way to compute pi?"
The main question is:

> can extrapolation remove the dominant polygon error term and improve convergence?

## Why this is interesting

Polygon methods are classical, geometric, and easy to reason about.

That makes them useful for:

- teaching numerical convergence
- studying rigorous upper/lower bounds
- experimenting with error cancellation
- comparing provable bounds against heuristic estimates

## How to run

Install dependencies first:

```bash
pip install mpmath matplotlib
```

Run the benchmark:

```bash
python benchmark.py
```

Plot the convergence curves:

```bash
python plot_extrapolation.py
```

## How to interpret results

- `lower` and `upper` are rigorous bounds
- `mid`, `R2`, and `R4` are estimates, not bounds
- if `R2` improves substantially over `mid`, that suggests the leading error
  term is being cancelled effectively
- in the current benchmark, `R2` is the meaningful improvement
- in the current benchmark, `R4` does not improve convergence and should be treated as a diagnostic, not a recommended estimator

## Comparison philosophy

`mp.pi` is used only as a trusted reference for measuring error.

It is **not** used inside the polygon method itself.

That separation matters: a candidate approximation method should not depend on
the exact value it is trying to approximate.

## Future directions

Reasonable next steps for this repo:

- derive the asymptotic error more carefully
- verify the observed convergence order analytically
- compare additional extrapolation schemes
- add timing comparisons across methods
- document where extrapolation helps and where it becomes unstable

## Current takeaway

The current benchmark suggests:

- midpoint error behaves like order `1/n^2`
- `R2` improves that to about order `1/n^4`
- `R4` is not useful here

So the main result is the `R2` acceleration, not the existence of multiple
equally good extrapolated estimators.

## Geometry-first takeaway

The current geometry-first benchmark suggests a stronger structure:

- perimeter midpoint error behaves like `+c / n^2`
- area midpoint error behaves like `-2c / n^2`
- blending them with `alpha = 2/3` cancels the leading `1/n^2` term
- that blend behaves like order `1/n^4`
- applying Richardson with `p = 4` to the blend produces an estimator with observed order `1/n^6`

This is the strongest result in the repo so far:

> perimeter midpoint -> order 2  
> `2/3` perimeter-area blend -> order 4  
> `R4` on that blend -> order 6

That is still not a challenge to Chudnovsky as a high-precision method, but it
is a respectable convergence-acceleration result for a geometry-first approach.

## Summary

RezPie is best understood as:

> a geometric and numerical experiment on polygon bounds for `pi`,
> with extrapolation used to study convergence acceleration.

That is a narrower claim than the original version of the project, but it is a
much stronger one.
