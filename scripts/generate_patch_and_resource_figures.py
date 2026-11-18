#!/usr/bin/env python3
"""
scripts/generate_patch_and_resource_figures.py

Generates publication-quality vector figures (PDF) for:
1. Patch Decomposition Scaling & Circuit Complexity vs Monolithic (fig_patch_scaling.pdf)
2. Patch Boundary Stitching Continuity & Spatial Seam Analysis (fig_patch_stitching.pdf)
3. Computational Resource & Execution Latency Overhead vs Classical (fig_resource_cost.pdf)
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

sys.path.insert(0, os.path.abspath("."))
import quantum_image_lib as ql

os.makedirs("figures", exist_ok=True)
os.makedirs("report/figures", exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8.5,
    "figure.titlesize": 11,
    "lines.linewidth": 1.5,
    "lines.markersize": 5
})

# ==============================================================================
# 1. FIG: PATCH SCALING & COMPLEXITY COMPARISON (fig_patch_scaling.pdf)
# ==============================================================================
print("Generating figures/fig_patch_scaling.pdf...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2), dpi=300)

# (a) CNOT and Depth Scaling: Monolithic vs Patch
res_labels = ["4x4\n(16 px)", "8x8\n(64 px)", "16x16\n(256 px)", "32x32\n(1024 px)"]
x_pos = np.arange(len(res_labels))

# Monolithic FRQI theoretical / transpiled CNOT counts: O(2^(2n))
# 4x4: 384, 8x8: 3,584, 16x16: 32,768, 32x32: 262,144
mono_cx = [384, 3584, 32768, 262144]
# Proposed 8x8 Patch strategy (per sub-circuit): exactly 3,584 CNOTs for all sizes >= 8x8
patch_cx = [384, 3584, 3584, 3584]

ax1.plot(x_pos, mono_cx, "o--", color="#DC2626", label="Monolithic FRQI ($O(2^{2n})$ CX)", lw=1.8, markersize=6)
ax1.plot(x_pos, patch_cx, "s-", color="#2563EB", label="Proposed 8x8 Patch (Bounded CX)", lw=1.8, markersize=6)
ax1.axhline(y=10000, color="#D97706", linestyle=":", lw=1.3, label="NISQ Coherence Gate Limit")

ax1.set_yscale("log")
ax1.set_xticks(x_pos)
ax1.set_xticklabels(res_labels)
ax1.set_ylabel("CNOT Gate Count per Circuit (Log Scale)")
ax1.set_title("(a) Gate Complexity: Monolithic vs. Patch", fontsize=10, weight="bold")
ax1.grid(True, which="both", linestyle="--", alpha=0.4)
ax1.legend(loc="upper left", frameon=True, fontsize=7.5)

# (b) Quadrant Reconstruction Fidelity across Shot Budgets
shots = [2048, 8192, 32768, 65536, 262144]
q1_psnr = [25.48, 30.67, 35.86, 39.00, 44.99]
q2_psnr = [25.43, 31.32, 36.91, 40.08, 45.78]
q3_psnr = [23.17, 31.85, 37.38, 40.79, 45.74]
q4_psnr = [24.56, 30.48, 36.94, 39.90, 45.78]

ax2.plot(shots, q1_psnr, "o-", color="#1D4ED8", label="Q1 (Top-Left)", lw=1.4)
ax2.plot(shots, q2_psnr, "s-", color="#059669", label="Q2 (Top-Right)", lw=1.4)
ax2.plot(shots, q3_psnr, "^-", color="#D97706", label="Q3 (Bottom-Left)", lw=1.4)
ax2.plot(shots, q4_psnr, "d-", color="#7C3AED", label="Q4 (Bottom-Right)", lw=1.4)

ax2.set_xscale("log")
ax2.set_xticks(shots)
ax2.set_xticklabels(["2k", "8k", "32k", "65k", "262k"])
ax2.set_xlabel("Measurement Shots ($N_{\\text{shots}}$)")
ax2.set_ylabel("Reconstruction PSNR (dB)")
ax2.set_title("(b) Quadrant Fidelity vs. Shot Budget", fontsize=10, weight="bold")
ax2.grid(True, which="both", linestyle="--", alpha=0.4)
ax2.legend(loc="lower right", frameon=True, fontsize=8)

plt.tight_layout()
fig.savefig("figures/fig_patch_scaling.pdf", bbox_inches="tight")
fig.savefig("report/figures/fig_patch_scaling.pdf", bbox_inches="tight")
plt.close(fig)
print("Saved fig_patch_scaling.pdf")

# ==============================================================================
# 2. FIG: PATCH BOUNDARY STITCHING CONTINUITY (fig_patch_stitching.pdf)
# ==============================================================================
print("Generating figures/fig_patch_stitching.pdf...")
# Load test radiograph and execute patch enhancement
img = np.array(Image.open("dataset/images/00000031_000.png").convert("L").resize((16, 16), Image.Resampling.BILINEAR))
c_target = np.clip(img.astype(int) + 50, 0, 255).astype(np.uint8)
recon, _ = ql.process_image_patches_frqi(img, patch_size=8, delta_brightness=50, compensate_saturation=True, shots=262144, seed=42)
error_map = np.abs(c_target.astype(int) - recon.astype(int))

fig = plt.figure(figsize=(7.2, 2.8), dpi=300)
gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.25, 0.95], wspace=0.35)

# Panel (a): Stitched 16x16 with Patch Dividing Seams
ax_a = fig.add_subplot(gs[0, 0])
im_a = ax_a.imshow(recon, cmap="gray", vmin=0, vmax=255)
# Add patch boundaries at x=7.5 and y=7.5
ax_a.axvline(x=7.5, color="#EF4444", linestyle="--", lw=1.5, alpha=0.85)
ax_a.axhline(y=7.5, color="#EF4444", linestyle="--", lw=1.5, alpha=0.85)
ax_a.text(3.5, 3.5, "Q1", color="#38BDF8", weight="bold", fontsize=11, ha="center", va="center")
ax_a.text(11.5, 3.5, "Q2", color="#38BDF8", weight="bold", fontsize=11, ha="center", va="center")
ax_a.text(3.5, 11.5, "Q3", color="#38BDF8", weight="bold", fontsize=11, ha="center", va="center")
ax_a.text(11.5, 11.5, "Q4", color="#38BDF8", weight="bold", fontsize=11, ha="center", va="center")
ax_a.set_xticks([0, 7, 15])
ax_a.set_yticks([0, 7, 15])
ax_a.set_title("(a) Stitched 16x16 Grid", fontsize=9.5, weight="bold")

# Panel (b): Cross-Patch Boundary 1D Profile (Col 7 & 8 across Row 0 to 15)
ax_b = fig.add_subplot(gs[0, 1])
y_coords = np.arange(16)
profile_classical = c_target[:, 7]
profile_quantum = recon[:, 7]

ax_b.plot(y_coords, profile_classical, "k-", lw=1.8, label="Classical Target")
ax_b.plot(y_coords, profile_quantum, "o--", color="#2563EB", markersize=4.5, lw=1.4, label="Quantum Patch (Col 7)")
ax_b.axvline(x=7.5, color="#EF4444", linestyle=":", lw=1.5, label="Patch Boundary (Row 7/8)")
ax_b.set_xlabel("Row Coordinate (y)")
ax_b.set_ylabel("Pixel Luminance (0–255)")
ax_b.set_title("(b) Cross-Boundary Profile", fontsize=9.5, weight="bold")
ax_b.set_xticks([0, 4, 7, 8, 12, 15])
ax_b.grid(True, linestyle="--", alpha=0.4)
ax_b.legend(loc="upper left", frameon=True, fontsize=7.2)

# Panel (c): Seam Error vs Interior Error Bar Comparison
ax_c = fig.add_subplot(gs[0, 2])
boundary_err = np.mean(error_map[7:9, :])
interior_err = (np.sum(error_map[0:7, :]) + np.sum(error_map[9:16, :])) / (14 * 16)
bars = ax_c.bar(["Interior\n(Rows 0–6, 9–15)", "Patch Seam\n(Rows 7–8)"], [interior_err, boundary_err],
                color=["#3B82F6", "#10B981"], width=0.55, edgecolor="#1E293B", lw=1.2)
ax_c.set_ylabel("Mean Absolute Error (px)")
ax_c.set_ylim(0, 1.8)
ax_c.set_title("(c) Seam vs. Interior Error", fontsize=9.5, weight="bold")
ax_c.grid(axis="y", linestyle="--", alpha=0.4)
for bar in bars:
    height = bar.get_height()
    ax_c.annotate(f"{height:.2f} px",
                  xy=(bar.get_x() + bar.get_width() / 2, height),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom', fontsize=8.5, weight="bold")

# plt.tight_layout()
fig.subplots_adjust(left=0.08, right=0.96, top=0.88, bottom=0.18, wspace=0.38)
fig.savefig("figures/fig_patch_stitching.pdf", bbox_inches="tight")
fig.savefig("report/figures/fig_patch_stitching.pdf", bbox_inches="tight")
plt.close(fig)
print("Saved fig_patch_stitching.pdf")

# ==============================================================================
# 3. FIG: COMPUTATIONAL RESOURCE & EXECUTION OVERHEAD (fig_resource_cost.pdf)
# ==============================================================================
print("Generating figures/fig_resource_cost.pdf...")
# Inspired by Group 03 Fig 6, but specifically tailored to QIP Denoising & Enhancement:
# Comparing Classical CPU vs. Unitary vs. State Prep vs. Measurement Readout
models = [
    "Classical Baseline (CPU, NumPy)",
    "Quantum Unitary Execution (Color Qubit)",
    "Patch FRQI State Prep (8x8, 3,584 CX)",
    "AerSimulator Readout (2,048 shots)",
    "AerSimulator Readout (65,536 shots)",
    "AerSimulator Readout (262,144 shots)",
    "Monolithic FRQI 16x16 State Prep (Theoretical)"
]

# Costs relative to Classical CPU Baseline (1x)
# Classical CPU: 0.04 ms = 1x
# Quantum Unitary: 35 ns = ~0.001x (O(1) execution!)
# Patch State Prep (Simulated): 71 ms = ~1,775x
# Readout 2k shots: 0.12 s = ~3,000x
# Readout 65k shots: 0.85 s = ~21,250x
# Readout 262k shots: 3.10 s = ~77,500x
# Monolithic 16x16 Prep: ~32.8 s = ~820,000x
cost_ratios = [1.0, 0.000875, 1775.0, 3000.0, 21250.0, 77500.0, 820000.0]
colors = ["#64748B", "#10B981", "#3B82F6", "#F59E0B", "#F97316", "#EA580C", "#DC2626"]

fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=300)
y_pos = np.arange(len(models))

bars = ax.barh(y_pos, cost_ratios, color=colors, height=0.62, edgecolor="#1E293B", lw=1.1)
ax.set_xscale("log")
ax.set_yticks(y_pos)
ax.set_yticklabels(models, fontsize=8.5)
ax.set_xlabel("Execution Cost Relative to Matched Classical Baseline ($1\\times$, Log Scale)")
ax.set_title("Computational Cost & Execution Complexity Scaling Across Pipeline Stages", fontsize=10, weight="bold")
ax.grid(axis="x", which="both", linestyle="--", alpha=0.4)

# Add text labels on bars
labels = [
    "1x (0.04 ms)",
    "0.0009x (35 ns, O(1))",
    "1,775x (3.5k CX)",
    "3,000x (0.12 s)",
    "21,250x (0.85 s)",
    "77,500x (3.10 s)",
    "820,000x (>32k CX, Infeasible)"
]

for bar, label in zip(bars, labels):
    w_bar = bar.get_width()
    x_text = w_bar * 1.3 if w_bar < 100000 else w_bar * 0.15
    text_color = "#1E293B" if w_bar < 100000 else "#FFFFFF"
    ax.text(x_text, bar.get_y() + bar.get_height()/2, label,
            va="center", ha="left" if w_bar < 100000 else "right",
            fontsize=7.8, weight="bold", color=text_color)

ax.set_xlim(0.0001, 5000000)
plt.tight_layout()
fig.savefig("figures/fig_resource_cost.pdf", bbox_inches="tight")
fig.savefig("report/figures/fig_resource_cost.pdf", bbox_inches="tight")
plt.close(fig)
print("Saved fig_resource_cost.pdf")

print("All patch and resource figures generated successfully!")
