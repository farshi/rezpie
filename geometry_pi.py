from mpmath import mp, sqrt

mp.dps = 100


def correct_digits(x, ref):
    err = abs(x - ref)
    if err == 0:
        return mp.inf
    return max(0, int(mp.floor(-mp.log10(err))))


def observed_order(err_n, err_2n):
    if err_n == 0 or err_2n == 0:
        return mp.inf
    return mp.log(err_n / err_2n, 2)


def richardson_extrapolate(a_n, a_2n, p: int):
    factor = mp.mpf(2) ** p
    return (factor * a_2n - a_n) / (factor - 1)


def blend_estimate(a, b, alpha):
    return alpha * a + (1 - alpha) * b


def derived_alpha():
    """
    Empirically, the perimeter midpoint has leading +c/n^2 error while the
    area midpoint has leading -2c/n^2 error. This blend cancels that term.
    """
    return mp.mpf(2) / 3


def perimeter_family(iterations: int = 16):
    n = 6
    s = mp.mpf(1)
    t = 2 / sqrt(3)
    rows = []

    for _ in range(iterations):
        lower = (n * s) / 2
        upper = (n * t) / 2
        mid = (lower + upper) / 2

        rows.append(
            {
                "n": n,
                "lower": lower,
                "upper": upper,
                "mid": mid,
                "width": upper - lower,
            }
        )

        s_next = sqrt(2 - sqrt(4 - s**2))
        t_next = (2 * s_next) / sqrt(4 - s_next**2)
        s = s_next
        t = t_next
        n *= 2

    return rows


def area_family(iterations: int = 16):
    n = 6
    s = mp.mpf(1)
    t = 2 / sqrt(3)
    rows = []

    for _ in range(iterations):
        a_in = sqrt(4 - s**2)
        a_out = mp.mpf(2)

        lower = (n * s * a_in) / 4
        upper = (n * t * a_out) / 4
        mid = (lower + upper) / 2

        rows.append(
            {
                "n": n,
                "lower": lower,
                "upper": upper,
                "mid": mid,
                "width": upper - lower,
            }
        )

        s_next = sqrt(2 - sqrt(4 - s**2))
        t_next = (2 * s_next) / sqrt(4 - s_next**2)
        s = s_next
        t = t_next
        n *= 2

    return rows


def grid_search_alpha(per_rows, area_rows, ref, step=0.01):
    best = None
    per_mid = per_rows[-1]["mid"]
    area_mid = area_rows[-1]["mid"]
    k = 0

    while k <= int(1 / step):
        alpha = mp.mpf(k) * step
        value = blend_estimate(per_mid, area_mid, alpha)
        err = abs(value - ref)

        if best is None or err < best["error"]:
            best = {
                "alpha": alpha,
                "value": value,
                "error": err,
                "digits": correct_digits(value, ref),
            }
        k += 1

    return best
