from mpmath import mp

from geometry_pi import (
    blend_estimate,
    area_family,
    correct_digits,
    derived_alpha,
    grid_search_alpha,
    observed_order,
    perimeter_family,
    richardson_extrapolate,
)

mp.dps = 100


def main():
    ref = mp.pi
    per_rows = perimeter_family(14)
    area_rows = area_family(14)

    print(f"Reference pi: {mp.nstr(ref, 40)}\n")

    print("Midpoint comparison")
    print(
        f"{'n':>8} "
        f"{'per err':>14} "
        f"{'area err':>14} "
        f"{'per digs':>9} "
        f"{'area digs':>9}"
    )

    per_mid_errors = []
    area_mid_errors = []
    for p_row, a_row in zip(per_rows, area_rows):
        per_err = abs(p_row["mid"] - ref)
        area_err = abs(a_row["mid"] - ref)
        per_mid_errors.append(per_err)
        area_mid_errors.append(area_err)

        print(
            f"{p_row['n']:8d} "
            f"{mp.nstr(per_err, 6):>14} "
            f"{mp.nstr(area_err, 6):>14} "
            f"{correct_digits(p_row['mid'], ref):9} "
            f"{correct_digits(a_row['mid'], ref):9}"
        )

    print("\nObserved midpoint order")
    print(f"{'n':>8} {'per order':>14} {'area order':>14}")
    for i in range(len(per_mid_errors) - 1):
        print(
            f"{per_rows[i]['n']:8d} "
            f"{mp.nstr(observed_order(per_mid_errors[i], per_mid_errors[i + 1]), 6):>14} "
            f"{mp.nstr(observed_order(area_mid_errors[i], area_mid_errors[i + 1]), 6):>14}"
        )

    print("\nRichardson extrapolation on midpoint (p=2)")
    print(
        f"{'n':>8} "
        f"{'per R2 err':>14} "
        f"{'area R2 err':>14} "
        f"{'per R2 digs':>12} "
        f"{'area R2 digs':>12}"
    )

    per_r2_errors = []
    area_r2_errors = []
    for i in range(len(per_rows) - 1):
        per_r2 = richardson_extrapolate(per_rows[i]["mid"], per_rows[i + 1]["mid"], 2)
        area_r2 = richardson_extrapolate(area_rows[i]["mid"], area_rows[i + 1]["mid"], 2)
        per_err = abs(per_r2 - ref)
        area_err = abs(area_r2 - ref)
        per_r2_errors.append(per_err)
        area_r2_errors.append(area_err)

        print(
            f"{per_rows[i]['n']:8d} "
            f"{mp.nstr(per_err, 6):>14} "
            f"{mp.nstr(area_err, 6):>14} "
            f"{correct_digits(per_r2, ref):12} "
            f"{correct_digits(area_r2, ref):12}"
        )

    print("\nObserved R2 order")
    print(f"{'n':>8} {'per R2 ord':>14} {'area R2 ord':>14}")
    for i in range(len(per_r2_errors) - 1):
        print(
            f"{per_rows[i]['n']:8d} "
            f"{mp.nstr(observed_order(per_r2_errors[i], per_r2_errors[i + 1]), 6):>14} "
            f"{mp.nstr(observed_order(area_r2_errors[i], area_r2_errors[i + 1]), 6):>14}"
        )

    best = grid_search_alpha(per_rows, area_rows, ref, step=0.01)
    print("\nBest perimeter/area midpoint blend")
    print(f"alpha       : {best['alpha']}")
    print(f"blend value : {mp.nstr(best['value'], 50)}")
    print(f"blend error : {mp.nstr(best['error'], 10)}")
    print(f"blend digits: {best['digits']}")

    alpha = derived_alpha()
    print("\nDerived blend alpha")
    print(f"alpha = 2/3 = {alpha}")

    print("\nBlend progression with alpha = 2/3")
    print(
        f"{'n':>8} "
        f"{'blend err':>14} "
        f"{'blend R4 err':>14} "
        f"{'blend digs':>12} "
        f"{'blend R4 digs':>14}"
    )
    blend_errors = []
    blend_r4_errors = []
    for p_row, a_row in zip(per_rows, area_rows):
        value = blend_estimate(p_row["mid"], a_row["mid"], alpha)
        err = abs(value - ref)
        blend_errors.append(err)
        print(
            f"{p_row['n']:8d} "
            f"{mp.nstr(err, 6):>14} "
            f"{'-':>14} "
            f"{correct_digits(value, ref):12} "
            f"{'-':>14}"
        )

    print("\nBlend R4 progression with alpha = 2/3")
    print(
        f"{'n':>8} "
        f"{'blend err':>14} "
        f"{'blend R4 err':>14} "
        f"{'blend digs':>12} "
        f"{'blend R4 digs':>14}"
    )
    for i in range(len(per_rows) - 1):
        blend = blend_estimate(per_rows[i]["mid"], area_rows[i]["mid"], alpha)
        blend_2n = blend_estimate(per_rows[i + 1]["mid"], area_rows[i + 1]["mid"], alpha)
        blend_r4 = richardson_extrapolate(blend, blend_2n, 4)
        err = abs(blend - ref)
        err_r4 = abs(blend_r4 - ref)
        blend_r4_errors.append(err_r4)
        print(
            f"{per_rows[i]['n']:8d} "
            f"{mp.nstr(err, 6):>14} "
            f"{mp.nstr(err_r4, 6):>14} "
            f"{correct_digits(blend, ref):12} "
            f"{correct_digits(blend_r4, ref):14}"
        )

    print("\nObserved blend orders (alpha = 2/3)")
    print(f"{'n':>8} {'blend ord':>14} {'blend R4 ord':>14}")
    for i in range(len(blend_r4_errors) - 1):
        print(
            f"{per_rows[i]['n']:8d} "
            f"{mp.nstr(observed_order(blend_errors[i], blend_errors[i + 1]), 6):>14} "
            f"{mp.nstr(observed_order(blend_r4_errors[i], blend_r4_errors[i + 1]), 6):>14}"
        )


if __name__ == "__main__":
    main()
