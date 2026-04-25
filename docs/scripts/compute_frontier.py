#!/usr/bin/env python3
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Synthetic example aligned with the LaTeX document
mu = np.array([0.12, 0.10, 0.07])
Sigma = np.array([
    [0.040, 0.006, 0.004],
    [0.006, 0.030, 0.002],
    [0.004, 0.002, 0.020],
])

ONE = np.ones(len(mu))
Sigma_inv = np.linalg.inv(Sigma)
A = ONE @ Sigma_inv @ ONE
B = ONE @ Sigma_inv @ mu
C = mu  @ Sigma_inv @ mu
D = A * C - B**2

# Risk-free rate for Sharpe example (optional)
r_f = 0.02

# Target return grid
r_min = float(mu.min()) * 0.95
r_max = float(mu.max()) * 1.05
targets = np.linspace(r_min, r_max, 40)

# Ensure build dir
ROOT = os.path.dirname(os.path.dirname(__file__))
BUILD = os.path.join(ROOT, "build")
os.makedirs(BUILD, exist_ok=True)

rows = []
risks = []
rets = []
sharpes = []
for r_star in targets:
    # Unconstrained Markowitz (sum w = 1, mu^T w = r*)
    w = ((C - B * r_star) / D) * (Sigma_inv @ ONE) + ((A * r_star - B) / D) * (Sigma_inv @ mu)
    ret = float(w @ mu)
    var = float(w @ Sigma @ w)
    std = np.sqrt(var)
    sharpe = (ret - r_f) / std if std > 0 else np.nan
    rows.append([
        r_star, ret, std, w[0], w[1], w[2], sharpe
    ])
    risks.append(std)
    rets.append(ret)
    sharpes.append(sharpe)

# Save CSV table (few selected points)
sel_targets = [0.075, 0.090, 0.105, 0.120, 0.135]
sel_rows = []
for r_star in sel_targets:
    w = ((C - B * r_star) / D) * (Sigma_inv @ ONE) + ((A * r_star - B) / D) * (Sigma_inv @ mu)
    ret = float(w @ mu)
    var = float(w @ Sigma @ w)
    std = np.sqrt(var)
    sharpe = (ret - r_f) / std if std > 0 else np.nan
    sel_rows.append([r_star, ret, std, w[0], w[1], w[2], sharpe])

csv_path = os.path.join(BUILD, "frontier_table.csv")
with open(csv_path, "w") as f:
    f.write("target_return,portfolio_return,portfolio_risk,w1,w2,w3,sharpe\n")
    for r in sel_rows:
        f.write(",".join(f"{x:.6f}" for x in r) + "\n")

# Also create LaTeX table rows for formatted inclusion
tex_rows_path = os.path.join(BUILD, "frontier_table.tex")
with open(tex_rows_path, "w") as f:
    for r_star, ret, std, w1, w2, w3, s in sel_rows:
        f.write(f"{r_star:.4f} & {ret:.4f} & {std:.4f} & {w1:.4f} & {w2:.4f} & {w3:.4f} & {s:.4f} \\\\ \n")

# Plot and save as PDF
fig, ax = plt.subplots(figsize=(6,4))
ax.plot(risks, rets, "-o", color="#1f77b4", markersize=3, linewidth=1)
# Annotate max Sharpe point
if len(sharpes) > 0 and np.isfinite(sharpes).any():
    idx = int(np.nanargmax(sharpes))
    ax.plot([risks[idx]], [rets[idx]], "s", color="#d62728", markersize=6, label="Sharpe max")
    ax.legend(loc="best")
ax.set_xlabel("Risque (écart-type)")
ax.set_ylabel("Rendement attendu")
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig_path_pdf = os.path.join(BUILD, "frontier_plot.pdf")
fig.savefig(fig_path_pdf)
print(f"Saved: {fig_path_pdf}\nSaved: {csv_path}\nSaved: {tex_rows_path}")
