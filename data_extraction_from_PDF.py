"""
I want to make different types of flashcards:
1. root-based:
    Front (Q): What does the root ten/tenu mean?
    Back (A): It means “thin.” \n example words: tenuous, attenuate

    and:

    Front: Which root means “thin”?
    Back: ten/tenu

2. Words meanings
    Front (Q): What does attenuate mean?
    Back (A): To make thin or slender; to weaken or reduce in force.


3. Example sentence
    Front: A ___ donor gave a large endowment to the university. (Which word fits?)
    Back: benevolent

4. Root of example word
    Front (Q): What is the root of attenuate?
    Back (A): ten/tenu.

"""

import fitz  # PyMuPDF
import re


# Open your PDF
doc = fitz.open("merriam-webster_s_vocabulary_builder.pdf")

num_units = 30


## Find all roots and add them to a list
def find_roots(doc, num_units):
    all_roots = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        page_lines = text.split("\n")
        # Check for a Unit header
        unit_match = True if page_lines[0].startswith("Unit") else False

        if unit_match:
            unit = int(page_lines[0].split(" ")[1])
            roots_line = page_lines[1]
            if roots_line:
                roots = re.findall(r"\b(?:[A-Z]+/?)+[A-Z]+\b", roots_line)
                all_roots.append(roots)
                continue
        if unit == num_units:
            break

    all_roots_flattened = [item for sublist in all_roots for item in sublist]
    return all_roots, all_roots_flattened


all_roots, all_roots_flat = find_roots(doc, num_units)
