import numpy as np
import matplotlib.pyplot as plt
import time

S0 = 100
K = 100
r = 0.04
sigma = 0.25
T = 3

def simulate_option_price(N, R, S0, K, r, sigma, T, seed):
    """Simulate an Asian option price using R paths and N time steps."""
    np.random.seed(seed)
    dt = T / N
    S = np.zeros((N+1, R))
    S[0] = S0
    for t in range(1, N+1):
        S[t] = S[t-1] * np.exp((r-0.5*sigma**2) * dt + sigma * np.sqrt(dt) * np.random.standard_normal(R))
    payoffs = np.maximum(np.mean(S, axis=0) - K, 0)
    discounted_payoffs = np.exp(-r*T) * payoffs
    price = np.mean(discounted_payoffs)
    se = np.std(discounted_payoffs, ddof=1) / np.sqrt(R)
    return price, se

N_fixed = 750  
Rs = [5000, 20000, 100000, 200000, 500000, 1000000]
for R in Rs:
    print(R)
    price_36, se_36 = simulate_option_price(36, R, S0, K, r, sigma, T, seed=0)
    price_150, se_150 = simulate_option_price(150, R, S0, K, r, sigma, T, seed=0)
    price_750, se_750 = simulate_option_price(750, R, S0, K, r, sigma, T, seed=0)
    diff_150_36 = abs(price_150 - price_36)
    se_diff_150_36 = np.sqrt(se_150**2 + se_36**2)
    margin_diff_150_36 = 1.96 * se_diff_150_36

    diff_750_150 = abs(price_750 - price_150)
    se_diff_750_150 = np.sqrt(se_750**2 + se_150**2)
    margin_diff_750_150 = 1.96 * se_diff_750_150

    if diff_150_36 > margin_diff_150_36 and diff_750_150 > margin_diff_750_150:
        print("Result: The difference is statistically significant at the 95% level.")
        break
print(diff_750_150,margin_diff_750_150,diff_150_36,margin_diff_150_36)
if diff_150_36 <= margin_diff_150_36 or diff_750_150 <= margin_diff_750_150:
    print("Result: The difference is not statistically significant for all R's ")

matrix_data = []

print(f"--- Testing R values for N={N_fixed} ---")
print(f"{'R (Paths)':<10} | {'Time (s)':<10} | {'Price':<10} | {'SE':<10} | {'95% Confidence Interval'}")
print("-" * 75)

for R in Rs:
    t0 = time.perf_counter()
    price, se = simulate_option_price(N_fixed, R, S0, K, r, sigma, T, seed=0)
    dt = time.perf_counter() - t0
    
    ci_margin = 1.96 * se
    ci_lower = price - ci_margin
    ci_upper = price + ci_margin
    
    matrix_data.append([R, dt, price, se, ci_margin])
    
    print(f"{R:<10} | {dt:<10.3f} | {price:<10.4f} | {se:<10.4f} | [{ci_lower:.4f}, {ci_upper:.4f}]")

# plots als we willen, is niet nodig denk ik voor dit, de tabel is al duidelijk genoeg, maar hier is de code:
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
Rs_vals = [row[0] for row in matrix_data]
ci_margins = [row[4] for row in matrix_data]
plt.plot(Rs_vals, ci_margins, marker='o', color='blue')
# Add red horizontal line showing the observed price difference and label it
plt.axhline(y=diff_150_36, color='red', linestyle='-', label='Price difference')
plt.xlabel('R (paths)')
plt.ylabel('95% CI Margin Size')
plt.title('Confidence Interval Margin vs R')
plt.grid(True, ls='--')
plt.legend()


plt.subplot(1, 2, 2)
plt.plot([row[0] for row in matrix_data], [row[1] for row in matrix_data], marker='o', color='red')
plt.xlabel('R (paths)')
plt.ylabel('Time (s)')
plt.title('Runtime vs R')
plt.grid(True, ls='--')

plt.tight_layout()
plt.show()

R_final = 1000000
Ns_assignment = [6, 36, 150, 750]

print(f"\n--- Final Results for R = {R_final} ---")
print(f"{'N (Steps)':<10} | {'Price':<10} | {'SE':<10} | {'95% Confidence Interval'}")
print("-" * 65)

for N in Ns_assignment:
    price, se = simulate_option_price(N, R_final, S0, K, r, sigma, T, seed=0)
    ci_margin = 1.96 * se
    ci_lower = price - ci_margin
    ci_upper = price + ci_margin
    print(f"{N:<10} | {price:<10.4f} | {se:<10.4f} | [{ci_lower:.4f}, {ci_upper:.4f}]")