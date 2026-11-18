#!/usr/bin/env python3
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, os.path.abspath("."))
import quantum_image_lib as ql

os.makedirs("figures", exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "figure.titlesize": 11
})

# ==============================================================================
# RE-DESIGN FIG A: SYSTEM ARCHITECTURE (2-Row Spacious Layout)
# ==============================================================================
print("Generating Fig A (2-row spacious layout)...")
fig, ax = plt.subplots(figsize=(7.2, 3.8))
ax.axis("off")

# 2 rows of 4 boxes
# Row 1: y = 0.56, height = 0.36
# Row 2: y = 0.08, height = 0.36
w = 0.20
h = 0.36
gap_x = 0.05
xs = [0.03 + i * (w + gap_x) for i in range(4)]

row1_boxes = [
    ("1. Input Data", "NIH ChestX-ray14\nThoracic Scans\n(1024x1024)", "#F8FAFC", "#475569"),
    ("2. Resampling", "Bilinear Scaling\nto 16x16 Grid\n(256 Pixels)", "#EFF6FF", "#3B82F6"),
    ("3. Denoising", "Selective QMF\nImpulse Noise\nSpike Purge", "#FEF3C7", "#D97706"),
    ("4. Partitioning", "Decomposition\ninto Four 8x8\nImage Patches", "#ECFDF5", "#059669")
]

row2_boxes = [
    ("8. Evaluation", "Fidelity Audit\nPSNR, SSIM, MSE\nError Heatmap", "#FEF2F2", "#DC2626"),
    ("7. Measurement", "AerSimulator\n262,144 Shots\nReadout Collapse", "#F5F3FF", "#7C3AED"),
    ("6. Transformation", "Unitary Gate\nPauli-X (Negative)\nRy(2Δθ) (Bright)", "#ECFDF5", "#059669"),
    ("5. State Prep", "Patch FRQI\n6 Pos + 1 Color\nUnitary Encoding", "#EFF6FF", "#2563EB")
]

# Draw Row 1 (Left to Right)
for i, (tag, text, bg, border) in enumerate(row1_boxes):
    x = xs[i]
    y = 0.58
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.025",
                                  facecolor=bg, edgecolor=border, linewidth=1.3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.08, tag, ha="center", va="center", fontsize=9, weight="bold", color=border)
    ax.text(x + w/2, y + 0.12, text, ha="center", va="center", fontsize=8, color="#1E293B", linespacing=1.2)
    
    # Arrow to next box in row 1
    if i < 3:
        ax.annotate("", xy=(xs[i+1] - 0.005, y + h/2), xytext=(x + w + 0.005, y + h/2),
                    arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#334155", mutation_scale=12))

# Arrow connecting Row 1 (box 4) to Row 2 (box 5, which is at xs[3])
ax.annotate("", xy=(xs[3] + w/2, 0.44 + 0.02), xytext=(xs[3] + w/2, 0.58 - 0.005),
            arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#334155", mutation_scale=12))

# Draw Row 2 (Right to Left: 5 -> 6 -> 7 -> 8)
# Box 5 is at xs[3], Box 6 at xs[2], Box 7 at xs[1], Box 8 at xs[0]
for idx, (tag, text, bg, border) in enumerate(row2_boxes):
    i = idx  # 0: box 8 at xs[0]; 1: box 7 at xs[1]; 2: box 6 at xs[2]; 3: box 5 at xs[3]
    x = xs[3 - idx]
    y = 0.08
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.025",
                                  facecolor=bg, edgecolor=border, linewidth=1.3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.08, tag, ha="center", va="center", fontsize=9, weight="bold", color=border)
    ax.text(x + w/2, y + 0.12, text, ha="center", va="center", fontsize=8, color="#1E293B", linespacing=1.2)
    
    # Arrow going left in row 2
    if idx < 3:
        next_x = xs[3 - idx - 1]
        ax.annotate("", xy=(next_x + w + 0.005, y + h/2), xytext=(x - 0.005, y + h/2),
                    arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#334155", mutation_scale=12))

ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.0)
plt.tight_layout()
fig.savefig("figures/fig_system_architecture.pdf", bbox_inches="tight")
plt.close(fig)
print("Saved figures/fig_system_architecture.pdf")

# ==============================================================================
# RE-DESIGN FIG B: WORKFLOW FLOWCHART (Vertical Structured Pipeline)
# ==============================================================================
print("Generating Fig B (Vertical Spacious Process Flow)...")
fig, ax = plt.subplots(figsize=(9.2, 5.4), dpi=300)
ax.axis("off")

stages = [
    ("Stage 1: Clinical Radiograph Preprocessing & Noise Model",
     "• Input: 1024x1024 frontal thoracic radiograph from official NIH ChestX-ray14 test split\n"
     "• Bilinear downsampling to 16x16 evaluation matrix (256 discrete pixel coordinates)\n"
     "• Impulse noise injection: 5% detector readout spikes (2.5% salt at I=255, 2.5% pepper at I=0)",
     0.78, "#EFF6FF", "#2563EB"),

    ("Stage 2: Selective Quantum Median Filtering (Denoising)",
     "• Physical impulse candidate tagging: conditionally identifies extreme bit-flip spikes (I ≤ 2 or I ≥ 253)\n"
     "• Spatial 3x3 rank-order sorting: emulates 3-qubit QCS comparator and Fredkin (CSWAP) sorting logic\n"
     "• Structural fidelity preservation: retains tissue margins while reducing cohort MSE from 714.24 to 66.93",
     0.53, "#FEF3C7", "#D97706"),

    ("Stage 3: FRQI Quantum State Preparation & Unitary Transformation",
     "• Matrix decomposition: four 8x8 non-overlapping spatial patches (6 position qubits + 1 color qubit each)\n"
     "• Angle encoding: continuous mapping θ = (I/255)(π/2) via multi-controlled Ry gates (3,584 CNOTs / patch)\n"
     "• Transformation on color qubit in O(1) gate time: Pauli-X (Negative) or Ry(2Δθ) (Brightness +25, +50, +75)",
     0.28, "#ECFDF5", "#059669"),

    ("Stage 4: AerSimulator Readout Sampling & Classical Matrix Reassembly",
     "• Realistic projective measurement sampling across shot budgets (2,048 up to 262,144 shots)\n"
     "• State angle recovery: θ = arcsin(√(P1)) where P1 = c1 / (c0 + c1); intensity I = round((2/π)θ * 255)\n"
     "• Patch reassembly: four 8x8 patches stitched into 16x16 output; benchmarked against classical targets",
     0.03, "#F5F3FF", "#7C3AED")
]

card_w = 0.94
card_h = 0.21
card_x = 0.03

for title, details, y_pos, bg, border in stages:
    rect = patches.FancyBboxPatch((card_x, y_pos), card_w, card_h, boxstyle="round,pad=0.012,rounding_size=0.025",
                                  facecolor=bg, edgecolor=border, linewidth=1.4)
    ax.add_patch(rect)
    ax.text(card_x + 0.025, y_pos + card_h - 0.042, title, ha="left", va="center",
            fontsize=10.0, weight="bold", color=border)
    ax.text(card_x + 0.025, y_pos + card_h - 0.122, details, ha="left", va="center",
            fontsize=8.0, color="#1E293B", linespacing=1.38)
    
    # Downward arrow to next card
    if y_pos > 0.1:
        ax.annotate("", xy=(card_x + card_w/2, y_pos - 0.036), xytext=(card_x + card_w/2, y_pos - 0.004),
                    arrowprops=dict(arrowstyle="-|>", lw=1.6, color="#475569", mutation_scale=12))

ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.03)
plt.tight_layout()
fig.savefig("figures/fig_workflow_flowchart.pdf", bbox_inches="tight")
plt.close(fig)
print("Saved figures/fig_workflow_flowchart.pdf")

# ==============================================================================
# RE-DESIGN FIG C: QUANTUM CIRCUITS (Clean Qiskit mpl, NO double titles)
# ==============================================================================
print("Generating Fig C (Clean circuit subplots with zero overlapping titles)...")
img_test_2x2 = np.array([[50, 100], [150, 200]], dtype=np.uint8)
qc_frqi_2x2, _, _ = ql.build_frqi_circuit(img_test_2x2)
qc_frqi_2x2 = ql.apply_quantum_negative(qc_frqi_2x2)

# Generate raw Qiskit circuit images WITHOUT any suptitle
fig_c1 = qc_frqi_2x2.draw("mpl", scale=0.85)
fig_c1.canvas.draw()
rgba1 = np.asarray(fig_c1.canvas.buffer_rgba())
plt.close(fig_c1)

qc_qcs = ql.build_quantum_comparator_circuit()
fig_c2 = qc_qcs.draw("mpl", scale=0.85)
fig_c2.canvas.draw()
rgba2 = np.asarray(fig_c2.canvas.buffer_rgba())
plt.close(fig_c2)

# Create clean combined figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 5.2), gridspec_kw={'height_ratios': [1.1, 0.9]})

ax1.imshow(rgba1)
ax1.axis("off")
ax1.set_title("(a) Canonical FRQI State Preparation Circuit with Single-Gate Pauli-X Transformation (2x2 Unit)",
              fontsize=9.5, weight="bold", pad=8)

ax2.imshow(rgba2)
ax2.axis("off")
ax2.set_title("(b) Elementary 3-Qubit Quantum Comparator and Conditional Swap (QCS) Unit",
              fontsize=9.5, weight="bold", pad=8)

plt.subplots_adjust(hspace=0.35)
plt.tight_layout()
fig.savefig("figures/fig_circuits.pdf", bbox_inches="tight")
plt.close(fig)
print("Saved figures/fig_circuits.pdf")
