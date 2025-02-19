from mpmath import mp, sin, tan, pi, exp, j

# Set precision to 200 decimal places
mp.dps = 200

def compute_pi_rezpie(max_iterations=1000):
    n = mp.mpf(6)  # Start with a hexagon
    for _ in range(max_iterations):
        pi_polygon = n * sin(pi / n)
        pi_extrapolated = 4 * tan(pi / n) / n
        tangent_correction = ((pi_extrapolated - pi_polygon) / (n**2) +
                               ((pi_extrapolated - pi_polygon) ** 2) / (2 * n**3) +
                               ((pi_extrapolated - pi_polygon) ** 3) / (3 * n**4))
        pi_optimized = pi_polygon + tangent_correction
        n *= 2
    return pi_optimized

def compute_pi_chudnovsky():
    return mp.pi

pi_rezpie = compute_pi_rezpie()
pi_chudnovsky = compute_pi_chudnovsky()

print(f"RezPie π: {pi_rezpie}")
print(f"Chudnovsky π: {pi_chudnovsky}")
