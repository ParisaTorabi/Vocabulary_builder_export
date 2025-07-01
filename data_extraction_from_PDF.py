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
    if (
        "Mythology" in lines[0]
        or "Latin" in lines[0]
        or "Greek" in lines[0]
        or "History" in lines[0]
    ):
        word_index = 1
    else:
        word_index = 0
    word = lines[word_index]

    paragraphs = []
    current_para = ""

    for _, line in enumerate(lines[word_index + 1 :]):
        stripped = line.strip()

        if not stripped:
            continue

        # If line ends in sentence punctuation, assume it's a paragraph break
        if re.search(r'[.!?]"?”?$', stripped):
            current_para += " " + stripped
            paragraphs.append(current_para.strip())
            current_para = ""
        else:
            current_para += " " + stripped  # Continue same paragraph

    # Catch any remaining paragraph
    if current_para.strip():
        paragraphs.append(current_para.strip())

    if paragraphs[0].startswith("(1)") and paragraphs[1].startswith("(2)"):
        paragraphs = [paragraphs[0] + " " + paragraphs[1]] + paragraphs[2:]

    return word, paragraphs


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
        if re.search(r'[.!?]"?”?$', stripped):
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


if __name__ == "__main__":
    all_roots, all_roots_flat = find_roots(doc, num_units)

    ### Create the root dataframe, including the columns root, definition, and example words
    root_columns = ["root", "meaning", "example_words"]
    root_df = pd.DataFrame(columns=root_columns)

    word_columns = ["word", "root", "definition", "sentence"]
    word_df = pd.DataFrame(columns=word_columns)

    current_pointer = 0
    seen_pages = []
    for i, page in enumerate(doc):
        if current_pointer == len(all_roots_flat):
            break
        else:
            current_root = all_roots_flat[current_pointer]

        text = page.get_text("text")
        page_lines = text.split("\n")
        # Check for a Unit header
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
            seen_pages.append(i)
            root_def = clean_and_reconstruct_root_paragraphs(
                text, current_root, unit_match
            )

            examples = ""
            for page_num in range(i + 1, i + 5):
                seen_pages.append(page_num)
                word_page = doc[page_num]
                text = word_page.get_text("text")
                example_word, word_data = clean_and_reconstruct_word_paragraphs(text)
                examples += " " + example_word
                word_definition = word_data[0]
                example_sentence = word_data[1]
                extended_def = " ".join(word_data[2:])
                word_df.loc[len(word_df)] = [
                    example_word,
                    current_root,
                    word_definition + "\n" + extended_def,
                    example_sentence,
                ]

            root_df.loc[len(root_df)] = [current_root, root_def, examples]
            current_pointer += 1

    for i, page in enumerate(doc):
        if i not in seen_pages:
            text = page.get_text("text")
            if "•" in text and "INTRODUCTION" not in text:
                example_word, word_data = clean_and_reconstruct_word_paragraphs(text)
                word_definition = word_data[0]
                example_sentence = word_data[1]
                extended_def = " ".join(word_data[2:])
                word_df.loc[len(word_df)] = [
                    example_word,
                    "--",
                    word_definition + "\n" + extended_def,
                    example_sentence,
                ]

    root_df.to_excel("roots_df.xlsx")
    word_df.to_excel("words_df.xlsx")
