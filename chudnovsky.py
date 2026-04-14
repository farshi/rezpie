from mpmath import mp


def chudnovsky_pi(terms: int = 8):
    total = mp.mpf(0)

    for k in range(terms):
        numer = mp.factorial(6 * k) * (13591409 + 545140134 * k)
        denom = (
            mp.factorial(3 * k)
            * mp.factorial(k) ** 3
            * (-262537412640768000) ** k
        )
        total += numer / denom

    return 426880 * mp.sqrt(10005) / total


if __name__ == "__main__":
    mp.dps = 100
    print(mp.nstr(chudnovsky_pi(8), 80))
