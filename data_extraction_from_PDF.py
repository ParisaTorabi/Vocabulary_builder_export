import fitz  # PyMuPDF
import re

# Open your PDF
doc = fitz.open("merriam-webster_s_vocabulary_builder.pdf")

num_roots = []
all_roots = []
num_units = 30

for i, page in enumerate(doc):

    text = page.get_text("text")
    # Check for a Unit header
    page_lines = text.split("\n")
    unit_match = True if page_lines[0].startswith("Unit") else False
    if unit_match:
        unit = int(page_lines[0].split(" ")[1])
        print(f"Detected Unit {unit}")
        roots_line = page_lines[1]
        if roots_line:
            roots = re.findall(r"\b(?:[A-Z]+/?)+[A-Z]+\b", roots_line)
            all_roots += roots
            num_roots.append(len(roots))
            print(f"Roots found: {roots}")
            continue
    if unit == num_units:
        break
