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
import pandas as pd

# Open your PDF
doc = fitz.open("merriam-webster_s_vocabulary_builder.pdf")

num_units = 30


# Given a "word page", clean and separate paragraphs.
# 1st paragraph: definition, 2nd: sentence, 3rd: Extended explanations.
def clean_and_reconstruct_word_paragraphs(text):
    lines = text.split("\n")
    paragraphs = []
    current_para = ""

    for _, line in enumerate(lines):
        stripped = line.strip()

        if not stripped:
            continue

        # If line ends in sentence punctuation, assume it's a paragraph break
        if re.search(r'[.!?]"?$', stripped):
            current_para += " " + stripped
            paragraphs.append(current_para.strip())
            current_para = ""
        else:
            current_para += " " + stripped  # Continue same paragraph

    # Catch any remaining paragraph
    if current_para.strip():
        paragraphs.append(current_para.strip())

    return paragraphs


# returns the definition of a root, given the root and whether or not it is the first root of a unit
def clean_and_reconstruct_root_paragraphs(text, root, unit_match):
    lines = text.split("\n")
    paragraphs = []
    current_para = ""
    began = False
    if unit_match:
        lines_to_search = lines[2:]
    else:
        lines_to_search = lines

    for line in lines_to_search:

        if not began and not line.startswith(root):
            continue
        else:
            began = True

        stripped = line.strip()

        if not stripped:
            continue
        # If line ends in sentence punctuation, assume it's a paragraph break
        if re.search(r'[.!?]"?$', stripped):
            current_para += " " + stripped
            paragraphs.append(current_para.strip())
            current_para = ""
        else:
            current_para += " " + stripped  # Continue same paragraph

    # Catch any remaining paragraph
    if current_para.strip():
        paragraphs.append(current_para.strip())

    return paragraphs[0]


## Find all roots and add them to a list
def find_roots(doc, num_units):
    all_roots = []
    unit = None
    for _, page in enumerate(doc):
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


### Create the root dataframe, including the columns root, definition, and example words
root_columns = ["root", "meaning", "example words"]
root_df = pd.DataFrame(columns=root_columns)
current_pointer = 0
for i, page in enumerate(doc):
    if current_pointer == len(all_roots_flat):
        break
    else:
        current_root = all_roots_flat[current_pointer]

    text = page.get_text("text")
    page_lines = text.split("\n")
    # Check for a root page
    unit_match = True if page_lines[0].startswith("Unit") else False
    root_match = (
        True
        if (
            page_lines[0].startswith(current_root)
            or unit_match
            or (len(page_lines) > 1 and page_lines[1].startswith(current_root))
        )
        else False
    )
    if root_match:
        root_def = clean_and_reconstruct_root_paragraphs(text, current_root, unit_match)
        examples = ""
        for page_num in range(i + 1, i + 5):
            word_page = doc[page_num]
            text = word_page.get_text("text")
            examples += (
                " " + clean_and_reconstruct_word_paragraphs(text)[0].split(" ")[0]
            )
        root_df.loc[len(root_df)] = [current_root, root_def, examples]
        current_pointer += 1

# print(root_df)
