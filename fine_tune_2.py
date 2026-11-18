#!/usr/bin/env python3

with open('report/main.tex') as f:
    text = f.read()

# Let's condense related_text slightly (Subsection B & D)
p_rel1 = text.find(r"\section{Related Work}")
p_rel2 = text.find(r"\section{Background and Problem Formulation}")
rel_chunk = text[p_rel1:p_rel2]

# Replace in related work
rel_chunk_new = rel_chunk.replace(
    r"coupling quantum comparators with Fredkin (controlled-swap, CSWAP) gates allows spatial window arrays to be sorted coherently in quantum memory. Despite their theoretical elegance, prior studies evaluated quantum filtering almost exclusively on synthetic binary silhouettes, leaving efficacy on complex clinical radiographs unexamined.",
    r"coupling quantum comparators with Fredkin (CSWAP) gates enables coherent sorting in quantum memory. However, prior studies evaluated quantum filtering strictly on synthetic silhouettes, leaving clinical radiographs unexamined."
)

rel_chunk_new = rel_chunk_new.replace(
    r"As evidenced by Table~I, existing QIP literature suffers from three gaps: (1) an overwhelming reliance on ideal mathematical simulations without physical measurement shot sampling; (2) an exclusive focus on artificial synthetic benchmark images lacking anatomical complexity; and (3) a complete decoupling of quantum denoising from quantum contrast enhancement. This paper bridges these critical gaps by delivering a fully integrated, NISQ-viable clinical pipeline validated on authentic human medical radiographs.",
    r"As shown in Table~I, prior QIP works exhibit three gaps: (1) reliance on ideal simulation without physical shot sampling; (2) focus on toy patterns lacking anatomical complexity; and (3) decoupling denoising from contrast enhancement. This paper bridges these gaps through a unified clinical pipeline on authentic radiographs."
)

# Condense Section V (Setup)
p_set1 = text.find(r"\section{Experimental Setup}")
p_set2 = text.find(r"\section{Results and Analysis}")
set_chunk = text[p_set1:p_set2]

set_chunk_new = set_chunk.replace(
    r"All quantum circuits are modeled, transpiled, and executed within Python 3.13 utilizing the official Qiskit 1.x open-source quantum framework \cite{qiskit2024}. Simulation of quantum state evolution is performed using Qiskit Aer 0.16 (\texttt{AerSimulator}), configured with fixed pseudorandom seeds (\texttt{seed=42}) to guarantee exact numerical reproducibility across runs. Classical matrix manipulations and ground-truth baselines are implemented in NumPy 2.2 and Pillow 11.0. Experiments were executed on an Apple Silicon M-series workstation configured with 16-core unified memory architecture.",
    r"All quantum circuits are transpiled and executed in Python 3.13 using Qiskit 1.x \cite{qiskit2024}. State simulations utilize Qiskit Aer 0.16 (\texttt{AerSimulator}) with seed=42 to guarantee exact numerical reproducibility. Baselines are implemented in NumPy 2.2 and Pillow 11.0 on an Apple Silicon workstation."
)

# Condense Section VI (Results)
p_res1 = text.find(r"\section{Results and Analysis}")
p_res2 = text.find(r"\section{Discussion}")
res_chunk = text[p_res1:p_res2]

res_chunk_new = res_chunk.replace(
    r"Under ideal statevector evolution (omitting measurement collapse), quantum state amplitudes are extracted directly from the statevector. Table~IV presents the quantitative comparison between classical and quantum transformations across all spatial resolutions.",
    r"Under ideal statevector evolution, quantum state amplitudes are extracted directly without measurement collapse. Table~IV summarizes classical and quantum metrics across resolutions."
)

res_chunk_new = res_chunk_new.replace(
    r"Table~VI and Fig.~3 decisively answer \textbf{RQ2}: On healthy tissue, the difference map is completely flat ($0.0$~px), proving high specificity. For the lung nodule, quantum enhancement produces an acute $23.0$~px detection hotspot directly over tumor coordinates. Pleural effusion and cardiomegaly yield $20.0$~px and $28.0$~px detection peaks, providing clinicians with sharply defined anatomical margins.",
    r"Table~VI and Fig.~3 decisively answer \textbf{RQ2}: Healthy tissue exhibits a flat zero-error difference map ($0.0$~px), confirming high specificity. For lung nodule cases, quantum enhancement produces an acute $23.0$~px detection hotspot over tumor coordinates, while effusion and cardiomegaly yield $20.0$~px and $28.0$~px detection peaks."
)

text = text[:p_rel1] + rel_chunk_new + text[p_rel2:]
p_set1 = text.find(r"\section{Experimental Setup}")
p_set2 = text.find(r"\section{Results and Analysis}")
text = text[:p_set1] + set_chunk_new + text[p_set2:]
p_res1 = text.find(r"\section{Results and Analysis}")
p_res2 = text.find(r"\section{Discussion}")
text = text[:p_res1] + res_chunk_new + text[p_res2:]

with open('report/main.tex', 'w') as f:
    f.write(text)

print("Applied fine tune 2!")
