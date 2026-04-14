# RezPie

RezPie is a small numerical-analysis project about approximating `pi` with
classical polygon bounds and simple extrapolation.

The focus is not on beating state-of-the-art high-precision algorithms.
The focus is on understanding convergence:

- how inscribed and circumscribed polygons bound `pi`
- how fast those bounds tighten
- whether extrapolation can improve a basic polygon estimate

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
- `R4`: an experimental higher-order extrapolation probe

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
- `R4` should be treated as experimental unless supported by stronger analysis

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

## Summary

RezPie is best understood as:

> a geometric and numerical experiment on polygon bounds for `pi`,
> with extrapolation used to study convergence acceleration.

That is a narrower claim than the original version of the project, but it is a
much stronger one.
