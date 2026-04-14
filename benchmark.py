from mpmath import mp

from rezpie import (
    polygon_bounds,
    richardson_extrapolate,
    correct_digits,
    observed_order,
)
from chudnovsky import chudnovsky_pi

mp.dps = 100


def benchmark_polygon(iterations: int = 14):
    ref = mp.pi
    rows = polygon_bounds(iterations)

    print("Polygon / extrapolation study")
    print("-----------------------------")
    print(
        f"{'n':>8} "
        f"{'mid err':>14} "
        f"{'R2 err':>14} "
        f"{'R4 err':>14} "
        f"{'mid digs':>9} "
        f"{'R2 digs':>9} "
        f"{'R4 digs':>9}"
    )

    mid_errors = []
    r2_errors = []
    r4_errors = []

    for i in range(len(rows) - 1):
        curr = rows[i]
        nxt = rows[i + 1]

        mid_n = curr["mid"]
        mid_2n = nxt["mid"]

        r2 = richardson_extrapolate(mid_n, mid_2n, p=2)
        r4 = richardson_extrapolate(mid_n, mid_2n, p=4)

        mid_err = abs(mid_n - ref)
        r2_err = abs(r2 - ref)
        r4_err = abs(r4 - ref)

        mid_errors.append(mid_err)
        r2_errors.append(r2_err)
        r4_errors.append(r4_err)

        print(
            f"{curr['n']:8d} "
            f"{mp.nstr(mid_err, 6):>14} "
            f"{mp.nstr(r2_err, 6):>14} "
            f"{mp.nstr(r4_err, 6):>14} "
            f"{correct_digits(mid_n, ref):9} "
            f"{correct_digits(r2, ref):9} "
            f"{correct_digits(r4, ref):9}"
        )

    print("\nObserved convergence order")
    print(
        f"{'n':>8} "
        f"{'mid order':>14} "
        f"{'R2 order':>14} "
        f"{'R4 order':>14}"
    )

    for i in range(len(mid_errors) - 1):
        print(
            f"{rows[i]['n']:8d} "
            f"{mp.nstr(observed_order(mid_errors[i], mid_errors[i + 1]), 6):>14} "
            f"{mp.nstr(observed_order(r2_errors[i], r2_errors[i + 1]), 6):>14} "
            f"{mp.nstr(observed_order(r4_errors[i], r4_errors[i + 1]), 6):>14}"
        )


def benchmark_chudnovsky():
    ref = mp.pi

    print("\nChudnovsky comparison")
    print("---------------------")
    print(f"{'terms':>8} {'error':>18} {'digits':>10}")

    for terms in [1, 2, 4, 6, 8]:
        value = chudnovsky_pi(terms)
        err = abs(value - ref)
        digs = correct_digits(value, ref)
        print(f"{terms:8d} {mp.nstr(err, 8):>18} {digs:10}")


if __name__ == "__main__":
    print(f"Reference pi: {mp.nstr(mp.pi, 40)}\n")
    benchmark_polygon()
    benchmark_chudnovsky()
