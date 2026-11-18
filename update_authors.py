with open("report/main.tex") as f:
    text = f.read()

# Replace author block
old_author = r"""\author{Group 05: Himanshu Sharma (Roll No. [UNVERIFIED: Roll No. 1]), Co-Author 1 (Roll No. [UNVERIFIED: Roll No. 2]), Co-Author 2 (Roll No. [UNVERIFIED: Roll No. 3]), Maheshwar Dwivedy, Kiran Khatter\\
School of Engineering \& Technology, BML Munjal University}"""

new_author = r"""\author{Group 09: Himanshu Sharma (Enrollment No. 230845), Vinit Yadav (Enrollment No. 230000), Maheshwar Dwivedy, Kiran Khatter\\
School of Engineering \& Technology (SOET), BML Munjal University}"""

text = text.replace(old_author, new_author)

# Replace Overleaf link
text = text.replace(
    r"\url{https://www.overleaf.com/project/group05_quantum_image_processing}",
    r"\url{https://www.overleaf.com/project/group09_quantum_image_processing}"
)

# Replace Author Contributions
old_contrib = r"""\section*{Author Contributions}
\textbf{Himanshu Sharma (Roll No. [UNVERIFIED: Roll No. 1]):} Designed the quantum circuit pipeline, implemented FRQI encoding and QMF modules in Qiskit, executed benchmarks across random seeds, and drafted the manuscript. \\
\textbf{Co-Author 1 (Roll No. [UNVERIFIED: Roll No. 2]):} Preprocessed the NIH ChestX-ray14 patient cohort, managed dataset stratification, and assisted with baseline classical implementations. \\
\textbf{Co-Author 2 (Roll No. [UNVERIFIED: Roll No. 3]):} Assisted with shot noise scaling experiments, figure generation scripts, and statistical validation."""

new_contrib = r"""\section*{Author Contributions}
\textbf{Himanshu Sharma (Enrollment No. 230845):} Conceived the study, designed the quantum circuit pipeline, implemented the FRQI encoding, unitary transformations, and QMF modules in Qiskit, executed benchmarks across random seeds, and drafted the manuscript. \\
\textbf{Vinit Yadav (Enrollment No. 230000):} Curated and stratified the NIH ChestX-ray14 200-patient test cohort, implemented baseline classical comparisons, executed finite-shot and brightness scaling experiments, and generated publication figures."""

text = text.replace(old_contrib, new_contrib)

with open("report/main.tex", "w") as f:
    f.write(text)

with open("main.tex", "w") as f:
    f.write(text)

print("Updated authors, enrollment numbers, SOET department, and group number successfully!")
