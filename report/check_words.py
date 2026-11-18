with open('report/main.tex') as f:
    text = f.read()

delimiters = [
    ("Abstract", r"\begin{abstract}", r"\end{abstract}", 200, 250),
    ("Section I: Introduction", r"\section{Introduction}", r"\section{Related Work}", 600, 800),
    ("Section II: Related Work", r"\section{Related Work}", r"\section{Background / Problem Formulation}", 700, 900),
    ("Section III: Background / Problem Formulation", r"\section{Background / Problem Formulation}", r"\section{Proposed Methodology}", 300, 500),
    ("Section IV: Proposed Methodology", r"\section{Proposed Methodology}", r"\section{Experimental Setup}", 900, 1200),
    ("Section V: Experimental Setup", r"\section{Experimental Setup}", r"\section{Results and Analysis}", 400, 600),
    ("Section VI: Results and Analysis", r"\section{Results and Analysis}", r"\section{Discussion}", 800, 1000),
    ("Section VII: Discussion", r"\section{Discussion}", r"\section{Conclusion and Future Work}", 300, 500),
    ("Section VIII: Conclusion and Future Work", r"\section{Conclusion and Future Work}", r"\section*{Code Availability}", 200, 300)
]

total = 0
print(f'{"SECTION":45s} | {"COUNT":7s} | {"TARGET":10s} | {"STATUS":8s}')
print('-' * 76)

for name, start_str, end_str, min_w, max_w in delimiters:
    p1 = text.find(start_str)
    p2 = text.find(end_str)
    if p1 != -1 and p2 != -1:
        chunk = text[p1 + len(start_str):p2]
        words = [w for w in chunk.split() if not w.startswith('\\') and not w.startswith('%')]
        count = len(words)
        total += count
        status = 'PASS' if (min_w * 0.9 <= count <= max_w * 1.1) else 'ADJUST'
        print(f'{name:45s} | {count:5d} w | {min_w}-{max_w:4d}   | {status:8s}')
    else:
        print(f'{name:45s} | NOT FOUND')

print('-' * 76)
print(f'TOTAL BODY WORDS (EXCLUDING REFERENCES): {total} words (Target: 4,500 - 5,500 words)')
