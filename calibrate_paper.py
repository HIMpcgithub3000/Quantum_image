#!/usr/bin/env python3

with open("report/main.tex") as f:
    text = f.read()

# 1. Trim Section I from 934 to ~720 words
p_s1 = text.find(r"\section{Introduction}")
p_s2 = text.find(r"\section{Related Work}")

sec1_calibrated = r"""Medical imaging represents a foundational pillar of modern clinical diagnostics, with thoracic radiography (chest X-rays) constituting one of the most frequently administered radiological examinations worldwide \cite{wang2017chestxray8}. Diagnostic utility depends directly on discerning subtle variations in photon attenuation between air-filled pulmonary parenchymal cavities, bony structures, and soft-tissue masses for automated detection of subtle pulmonary opacities and infiltrates \cite{rajpurkar2017chexnet}. Under clinical protocols governed by the ALARA (As Low As Reasonably Achievable) principle, digital radiograph detector plates intentionally operate in photon-starved regimes to minimize patient radiation exposure. Consequently, raw radiographs frequently exhibit restricted dynamic range, compressed contrast gradients, and low background luminance \cite{boyat2015review}. Under these imaging constraints, faint pulmonary opacities and shallow pleural effusions present with optical contrast differentials of fewer than ten grayscale levels, increasing false-negative risks. Furthermore, detector plates are prone to capacitive readout spikes and thermal drift, injecting high-amplitude impulse noise ($I \in \{0, 255\}$) that classical sharpening algorithms inadvertently amplify into synthetic lesion artifacts.

Existing classical computer vision approaches to medical image enhancement are fundamentally bounded by Von Neumann memory architectures. In classical digital processing, an $N \times N$ radiograph is stored in random-access memory as an array of $N^2$ independent numerical values. Any global spatial-domain transformation---such as linear contrast stretching, histogram equalization, or pixel inversion---must traverse all $N^2$ memory locations sequentially or via raster blocks, imposing an algorithmic time complexity of $O(N^2)$ \cite{caraiman2014image}. While GPUs accelerate raster operations through multi-threaded parallelism, high-throughput hospital picture archiving and communication systems (PACS) face escalating memory bandwidth bottlenecks and power dissipation budgets \cite{hu2019quantum}. Furthermore, classical spatial filtering techniques rely on spatial neighborhood convolutions that can blur acute anatomical boundaries, reducing margin sharpness.

Quantum Image Processing (QIP) provides an alternative computational paradigm that addresses both representation scaling and transformation time complexities \cite{venegas2012quantum, yan2017survey}. By exploiting quantum superposition, entanglement, and unitary linear transformations, digital images can be mapped into normalized Hilbert state spaces \cite{le2011flexible, zhang2013neqr}. Under the Flexible Representation of Quantum Images (FRQI) model established by Le et al. \cite{le2011flexible}, a two-dimensional grid of $2^n \times 2^n$ pixels is addressed using $2n$ position qubits in uniform superposition, with continuous grayscale intensities stored as trigonometric probability amplitudes on a single auxiliary color qubit. This formulation addresses an $N \times N$ image matrix containing $N^2$ classical pixels using only $2\log_2 N + 1$ qubits, achieving exponential spatial coordinate compression in register width. More importantly, because all spatial coordinates coexist simultaneously within a coherent superposition state, any unitary single-qubit quantum gate applied to the color qubit acts concurrently across all $N^2$ pixel basis states, collapsing the gate cost of global intensity transformations from classical $O(N^2)$ steps down to an instantaneous $O(1)$ single-gate execution post-state-prep \cite{le2011flexible, wang2020quantum}.

However, deploying QIP algorithms to real-world medical datasets presents distinct challenges under the Noisy Intermediate-Scale Quantum (NISQ) era \cite{preskill2018quantum}. Monolithic FRQI state preparation circuits require multi-controlled rotation gates whose decomposed CNOT gate counts scale exponentially ($O(2^{2n})$), rapidly exceeding hardware coherence times ($T_1, T_2$) and inducing state decoherence \cite{cross2019validating}. Furthermore, quantum states cannot be read out deterministically; physical wavefunction collapse requires repeated projective measurements (shots), introducing statistical shot noise that can degrade radiological detail \cite{bravyi2021error}. Finally, prior QIP literature has largely evaluated synthetic silhouettes, leaving quantitative behavior on authentic human thoracic radiographs unexamined.

To investigate these questions systematically, this paper addresses two primary research questions:
\begin{itemize}
    \item \textbf{RQ1:} Can an FRQI-based quantum circuit pipeline execute intensity-based contrast transformations on thoracic radiographs with $O(1)$ gate cost post-state-prep while maintaining structural fidelity above $98\%$ relative to classical numerical baselines under realistic finite measurement sampling?
    \item \textbf{RQ2:} Can a pre-enhancement Quantum Median Filter (QMF) modeling quantum comparator and conditional-swap networks suppress detector impulse noise spikes without introducing anatomical distortion or severe blurring on authentic human radiographs?
\end{itemize}

In addressing these questions, our paper makes four main contributions:
\begin{enumerate}
    \item \textbf{End-to-End Clinical QIP Pipeline on NIH ChestX-ray14:} We design and execute a complete quantum image processing workflow in Qiskit evaluated on 200 unique patient radiographs from the official held-out test split of the NIH ChestX-ray14 dataset across three random seeds (42, 43, 44).
    \item \textbf{Analysis of Pre-Enhancement Quantum Median Filtering:} We evaluate a selective median filter modeling 3-qubit quantum comparator and Fredkin (CSWAP) sorting cells, demonstrating a reduction in MSE from $714.24 \pm 279.71$ to $66.93 \pm 92.98$ and a PSNR gain of $+12.60$~dB over unfiltered enhancement across all 200 patients.
    \item \textbf{NISQ-Oriented Patch Decomposition Strategy:} We implement an $8\times8$ spatial patch decomposition that bounds quantum circuit depth to 3,584 CNOT gates per sub-circuit, avoiding high-depth decoherence limits while enabling global $R_y(2\Delta\theta)$ contrast shifts with SSIM of $0.9995 \pm 0.0001$.
    \item \textbf{Defensible Characterization of Quantum Costs and Bounds:} We characterize the distinction between the $O(1)$ unitary transformation gate cost and the non-$O(1)$ state preparation ($O(2^{2n})$ CNOTs) and finite-shot readout sampling ($1/\sqrt{N_{\text{shots}}}$ variance), delineating practical boundaries for NISQ medical image simulation.
\end{enumerate}

The remainder of this paper is structured as follows: Section II surveys related work. Section III defines notation and problem formulation. Section IV details methodology and circuits. Section V outlines experimental setup. Section VI presents empirical results. Section VII discusses implications and limitations. Section VIII concludes the paper."""

# 2. Expand Section IV (Methodology) from 784 to ~980 words
p_s4 = text.find(r"\section{Proposed Methodology}")
p_s5 = text.find(r"\section{Experimental Setup}")

sec4_calibrated = r"""This section details the proposed quantum image processing methodology, circuit architectures, mathematical transformations, and algorithmic implementation.

\subsection{System Architecture and Processing Pipeline}
The end-to-end architecture of the proposed pipeline is illustrated in Fig.~1. The framework comprises four interconnected functional stages: (1) radiograph downsampling and noise modeling, (2) spatial filtering via selective quantum median filtering, (3) patch-based FRQI quantum state preparation and unitary transformation, and (4) projective measurement readout and classical image matrix reconstruction.

\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_system_architecture.pdf}
\caption{System architecture of the proposed quantum image processing pipeline. Raw clinical radiographs are downsampled to $16\times16$, processed by a selective QMF stage to purge detector readout spikes, encoded into patch-based FRQI quantum states, transformed via single-qubit unitary operations, and reconstructed through projective measurement sampling on AerSimulator.}
\label{fig:architecture}
\end{figure}

Fig.~2 illustrates the operational workflow flowchart with parameter configurations and data dimensionality at each step of the pipeline. The workflow begins with a full-resolution $1024 \times 1024$ chest radiograph, downsampled bilinearly to $16 \times 16$, corrupted by a $5\%$ impulse noise model to simulate detector readout failure, filtered via the QMF stage, decomposed into four $8 \times 8$ non-overlapping spatial patches, transpiled into Qiskit circuits, executed across $N_{\text{shots}}$ measurements, and reconstructed into an 8-bit enhanced grayscale image.

\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_workflow_flowchart.pdf}
\caption{Operational workflow flowchart indicating data flow, dimensionality, and parameters across the four processing stages: preprocessing, denoising, quantum transformation, and measurement recovery.}
\label{fig:workflow}
\end{figure}

\subsection{FRQI Quantum Image State Preparation}
In the Flexible Representation of Quantum Images (FRQI) model formulated by Le et al. \cite{le2011flexible}, grayscale pixel intensities $I(y, x) \in [0, 255]$ are converted to continuous rotation angles $\theta_i \in [0, \pi/2]$:
\begin{equation}
\theta_i = \frac{I(y, x)}{255} \cdot \frac{\pi}{2}, \quad i = y \cdot N + x
\end{equation}
The composite quantum state $|I(\theta)\rangle$ is defined across $2n$ position qubits and 1 color qubit:
\begin{equation}
|I(\theta)\rangle = \frac{1}{2^n} \sum_{i=0}^{2^{2n}-1} |i\rangle \otimes (\cos\theta_i |0\rangle + \sin\theta_i |1\rangle)
\end{equation}
State preparation begins with the ground state $|0\rangle^{\otimes 2n} \otimes |0\rangle$. A parallel layer of Hadamard gates $H^{\otimes 2n}$ creates uniform spatial superposition across all $2^{2n}$ pixel coordinates:
\begin{equation}
H^{\otimes 2n} |0\rangle^{\otimes 2n} = \frac{1}{2^n} \sum_{i=0}^{2^{2n}-1} |i\rangle
\end{equation}
Next, multi-controlled rotation gates $C^{2n}(R_y(2\theta_i))$ rotate the color qubit conditioned on coordinate basis state $|i\rangle$. The rotation angle is doubled ($2\theta_i$) because a rotation gate $R_y(\alpha)$ on state $|0\rangle$ produces $\cos(\alpha/2)|0\rangle + \sin(\alpha/2)|1\rangle$; thus setting $\alpha = 2\theta_i$ accurately sets the amplitude coefficients to $\cos\theta_i$ and $\sin\theta_i$. The canonical $2\times2$ FRQI state preparation circuit is depicted in Fig.~3(a), showing how coordinate control lines conditionally trigger the color qubit rotation.

\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/fig_circuits.pdf}
\caption{Quantum circuit architectures. (a) Canonical 2-position qubit ($2\times2$) FRQI state preparation circuit followed by a single-qubit Pauli-$X$ photographic negative gate. (b) Elementary 3-qubit Quantum Comparator and Conditional Swap (QCS) unit constructed from Pauli-$X$, Toffoli (CCX), and Fredkin (CSWAP) gates.}
\label{fig:circuits}
\end{figure}

\subsection{Selective Quantum Median Filtering (QMF)}
Detector impulse noise spikes ($I \in \{0, 255\}$) present severe non-linear distortion. In quantum sorting networks \cite{wang2022quantum}, sorting spatial neighborhoods requires quantum comparator units. Fig.~3(b) depicts the elementary 3-qubit Quantum Comparator \& Conditional Swap (QCS) cell. It operates on two data qubits ($|a\rangle, |b\rangle$) and an ancilla ($|\text{comp}\rangle$):
\begin{enumerate}
    \item $X(b)$ inverts qubit $b$.
    \item A Toffoli gate $CCX(a, b, \text{comp})$ sets $|\text{comp}\rangle = |1\rangle$ if and only if $a=1$ and $b=0$ (i.e., $a > b$).
    \item $X(b)$ restores qubit $b$.
    \item A Fredkin gate $CSWAP(\text{comp}, a, b)$ swaps states $|a\rangle$ and $|b\rangle$ if $\text{comp}=1$, yielding $|min(a, b)\rangle$ and $|max(a, b)\rangle$.
\end{enumerate}
Transpiling this unit reveals exactly 14 CNOT gates and a circuit depth of 25. In our software implementation, evaluating full 8-bit quantum sorting across a $3\times3$ spatial neighborhood requires $9 \times 8 = 72$ data qubits plus comparison ancillae, which exceeds classical simulator memory. Therefore, our pipeline implements a selective median filter modeling the QCS sorting logic: impulse candidate pixels ($I \le 2$ or $I \ge 253$) are selectively identified and replaced with the neighborhood median, leaving genuine anatomical tissue gradients completely unmodified and preventing unnecessary edge blurring.

\subsection{Unitary Transformations and Saturation Management}
Following state preparation, intensity transformations are applied directly to the color qubit:
\begin{itemize}
    \item \textbf{Quantum Photographic Negative:} A single Pauli-$X$ gate swaps $|0\rangle \leftrightarrow |1\rangle$:
    \begin{equation}
    X (\cos\theta_i |0\rangle + \sin\theta_i |1\rangle) = \sin\theta_i |0\rangle + \cos\theta_i |1\rangle = \cos(\pi/2 - \theta_i) |0\rangle + \sin(\pi/2 - \theta_i) |1\rangle
    \end{equation}
    This simultaneously maps $I_i \mapsto 255 - I_i$ for all $N^2$ pixels in $O(1)$ gate execution.
    \item \textbf{Quantum Brightness Enhancement:} An $R_y(2\Delta\theta)$ gate rotates the color qubit by angle $\Delta\theta = (\Delta / 255)(\pi / 2)$:
    \begin{equation}
    R_y(2\Delta\theta) |c\rangle = \cos(\theta_i + \Delta\theta) |0\rangle + \sin(\theta_i + \Delta\theta) |1\rangle
    \end{equation}
    To prevent trigonometric wrap-around when $\theta_i + \Delta\theta > \pi/2$, angles are saturated as $\theta'_i = \min(\theta_i + \Delta\theta, \pi/2)$. In our patch pipeline, this saturation constraint is enforced during target preparation prior to patch unitary application, ensuring linear intensity shifts without trigonometric distortion.
\end{itemize}

\subsection{NISQ Patch Decomposition and Shot-Based Readout}
Monolithic FRQI on a $16\times16$ grid requires 9 qubits and over $20,000$ decomposed CNOT gates, which severely degrades state coherence in NISQ settings. To resolve this, we decompose the $16\times16$ matrix into four non-overlapping $8\times8$ sub-patches. Each patch requires 7 qubits (6 position, 1 color) and exactly 3,584 CNOT gates, bounding circuit depth.

During readout, projective measurement collapses the wavefunction. For pixel $i$, observing counts $c_0(i)$ and $c_1(i)$ across $N_{\text{shots}}$ yields:
\begin{equation}
\hat{P}_1(i) = \frac{c_1(i)}{c_0(i) + c_1(i)}, \quad \hat{\theta}_i = \arcsin\left(\sqrt{\hat{P}_1(i)}\right)
\end{equation}
The reconstructed intensity is recovered via $\hat{I}(y, x) = \text{round}\left(\frac{2}{\pi} \hat{\theta}_i \cdot 255\right)$. Algorithm~1 formalizes the complete execution sequence."""

# 3. Expand Section VIII (Conclusion) from 116 to ~230 words
p_s8 = text.find(r"\section{Conclusion and Future Work}")
p_s_disc = text.find(r"\section*{Code Availability}")

sec8_calibrated = r"""In this paper, we presented the design, implementation, and empirical validation of an end-to-end quantum image processing pipeline based on the Flexible Representation of Quantum Images (FRQI) for low-contrast thoracic radiographs.

In answering \textbf{RQ1}, our findings demonstrate that single-qubit unitary transformations achieve exact mathematical parity with classical numerical baselines under ideal statevector simulation ($\text{PSNR} = 100.00 \pm 0.00$~dB, $\text{SSIM} = 1.0000 \pm 0.0000$, $\text{MSE} = 0.00 \pm 0.00$), and maintain structural fidelity above $99.9\%$ ($\text{SSIM} = 0.9995 \pm 0.0001$, $\text{PSNR} = 45.78 \pm 0.53$~dB at $262{,}144$ shots) under realistic projective measurement sampling. We clarified that while the intensity transformation executes in $O(1)$ single-gate time on the color qubit, state preparation and measurement readout scale non-$O(1)$, following an empirical $1/\sqrt{N_{\text{shots}}}$ sampling convergence.

In answering \textbf{RQ2}, comprehensive evaluation across a held-out cohort of 200 unique patient radiographs from the official NIH ChestX-ray14 dataset under three random seeds (42, 43, 44) confirmed that integrating a pre-enhancement selective Quantum Median Filter (QMF) successfully suppresses detector readout spikes. The QMF stage reduces cohort Mean Squared Error from $714.24 \pm 279.71$ (unfiltered enhancement) to $66.93 \pm 92.98$ (a $90.6\%$ reduction), elevates average PSNR by $+12.60$~dB to $32.57 \pm 4.70$~dB, and increases SSIM to $0.991 \pm 0.009$, without blurring anatomical margins.

Future research directions include deploying our patch circuits on physical superconducting quantum hardware, exploring compressed quantum state preparation routines to mitigate CNOT gate depth, and interfacing enhanced quantum image states directly with parameterized quantum circuits for downstream clinical classification."""

text = text[:p_s1 + len(r"\section{Introduction}")] + "\n" + sec1_calibrated + "\n" + text[p_s2:]

p_s4 = text.find(r"\section{Proposed Methodology}")
p_s5 = text.find(r"\section{Experimental Setup}")
text = text[:p_s4 + len(r"\section{Proposed Methodology}")] + "\n" + sec4_calibrated + "\n" + text[p_s5:]

p_s8 = text.find(r"\section{Conclusion and Future Work}")
p_s_disc = text.find(r"\section*{Code Availability}")
text = text[:p_s8 + len(r"\section{Conclusion and Future Work}")] + "\n" + sec8_calibrated + "\n" + text[p_s_disc:]

with open("report/main.tex", "w") as f:
    f.write(text)

with open("main.tex", "w") as f:
    f.write(text)

print("Calibrated main.tex successfully!")
