from mpmath import mp, sqrt


def polygon_bounds(iterations: int = 20):
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


def richardson_extrapolate(a_n, a_2n, p: int):
    factor = mp.mpf(2) ** p
    return (factor * a_2n - a_n) / (factor - 1)


def correct_digits(x, ref):
    err = abs(x - ref)
    if err == 0:
        return mp.inf
    return max(0, int(mp.floor(-mp.log10(err))))


def observed_order(err_n, err_2n):
    if err_n == 0 or err_2n == 0:
        return mp.inf
    return mp.log(err_n / err_2n, 2)
