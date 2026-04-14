import matplotlib.pyplot as plt
from mpmath import mp

from rezpie import polygon_bounds, richardson_extrapolate

mp.dps = 100


def main():
    ref = mp.pi
    rows = polygon_bounds(16)

    xs = []
    mid_errs = []
    r2_errs = []
    r4_errs = []
    widths = []

    for i in range(len(rows) - 1):
        curr = rows[i]
        nxt = rows[i + 1]

        r2 = richardson_extrapolate(curr["mid"], nxt["mid"], p=2)
        r4 = richardson_extrapolate(curr["mid"], nxt["mid"], p=4)

        xs.append(curr["n"])
        mid_errs.append(float(abs(curr["mid"] - ref)))
        r2_errs.append(float(abs(r2 - ref)))
        r4_errs.append(float(abs(r4 - ref)))
        widths.append(float(curr["width"]))

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    ax[0].plot(xs, mid_errs, marker="o", label="midpoint")
    ax[0].plot(xs, r2_errs, marker="o", label="R2")
    ax[0].plot(xs, r4_errs, marker="o", label="R4")
    ax[0].set_xscale("log", base=2)
    ax[0].set_yscale("log")
    ax[0].set_xlabel("polygon sides")
    ax[0].set_ylabel("absolute error")
    ax[0].set_title("Error vs polygon size")
    ax[0].legend()

    ax[1].plot(xs, widths, marker="o", label="bound width")
    ax[1].set_xscale("log", base=2)
    ax[1].set_yscale("log")
    ax[1].set_xlabel("polygon sides")
    ax[1].set_ylabel("upper - lower")
    ax[1].set_title("Rigorous bound width")
    ax[1].legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
