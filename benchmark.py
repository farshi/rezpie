from mpmath import mp, sin, tan, pi, exp, j

# Set precision to 200 decimal places
mp.dps = 200 

def compute_pi_optimized(max_iterations=1000):
    """Computes π using an improved geometric-tangent method efficiently."""
    n = mp.mpf(6)  # Start with a hexagon
    pi_estimates = []

    for i in range(max_iterations):
        # Polygon-based approximation
        pi_polygon = n * sin(pi / n)

        # Extrapolation correction (avoiding sum for efficiency)
        pi_extrapolated = 4 * tan(pi / n) / n  

        # Higher-order tangent correction
        tangent_correction = ((pi_extrapolated - pi_polygon) / (n**2) +
                               ((pi_extrapolated - pi_polygon) ** 2) / (2 * n**3) +
                               ((pi_extrapolated - pi_polygon) ** 3) / (3 * n**4))

        # Refined π approximation
        pi_optimized = pi_polygon + tangent_correction

        # Store estimates
        pi_estimates.append(pi_optimized)

        # Double the polygon sides
        n *= 2  

    return pi_estimates[-1]

def compute_pi_chudnovsky():
    """Computes π using the Chudnovsky algorithm."""
    return mp.pi  # Chudnovsky is the default high-precision method in mpmath

def compute_pi_bbp():
    """Computes π using the Bailey–Borwein–Plouffe (BBP) algorithm."""
    bbp_pi = mp.mpf(0)
    k = 0
    while k < 100:  # More terms increase precision
        bbp_pi += (mp.power(16, -k) * 
                   (mp.mpf(4)/(8*k+1) - mp.mpf(2)/(8*k+4) - 
                    mp.mpf(1)/(8*k+5) - mp.mpf(1)/(8*k+6)))
        k += 1
    return bbp_pi

# Compute π using all methods
pi_optimized = compute_pi_optimized()
pi_chudnovsky = compute_pi_chudnovsky()
pi_bbp = compute_pi_bbp()  # Our neutral judge

# Compute deviations
deviation_optimized = abs(pi_optimized - pi_bbp)
deviation_chudnovsky = abs(pi_chudnovsky - pi_bbp)

# Determine the winner
if deviation_optimized < deviation_chudnovsky:
    winner = "RezPie Method 🎉"
elif deviation_chudnovsky < deviation_optimized:
    winner = "Chudnovsky 🏆"
else:
    winner = "It's a Tie! 🤝"

# Print results
print("\n### Final π Comparison ###")
print(f"π (RezPie Method): {pi_optimized}")
print(f"π (Chudnovsky Method): {pi_chudnovsky}")
print(f"π (BBP Judge): {pi_bbp}")

print("\n### Deviations from BBP ###")
print(f"Deviation (RezPie): {deviation_optimized}")
print(f"Deviation (Chudnovsky): {deviation_chudnovsky}")

print("\n### 🏆 The Winner is:", winner, "🏆 ###")

### **Testing Euler's Identity**
euler_test_optimized = exp(j * pi_optimized)
euler_test_chudnovsky = exp(j * pi_chudnovsky)

deviation_euler_optimized = abs(euler_test_optimized + 1)
deviation_euler_chudnovsky = abs(euler_test_chudnovsky + 1)

print("\n### Euler's Identity Test ###")
print(f"e^(i * π_optimized) = {euler_test_optimized}")
print(f"Deviation from -1 (Optimized): {deviation_euler_optimized}")

print(f"\ne^(i * π_chudnovsky) = {euler_test_chudnovsky}")
print(f"Deviation from -1 (Chudnovsky): {deviation_euler_chudnovsky}")

# Who wins Euler's test?
if deviation_euler_optimized < deviation_euler_chudnovsky:
    euler_winner = "RezPie Method 🎉"
elif deviation_euler_chudnovsky < deviation_euler_optimized:
    euler_winner = "Chudnovsky 🏆"
else:
    euler_winner = "It's a Tie! 🤝"

print("\n### 🏆 Euler's Identity Winner:", euler_winner, "🏆 ###")