"""
I want to make different types of flashcards:
1. root-based:
    Front (Q): What does the root ten/tenu mean?
    Back (A): It means “thin.” \n example words: tenuous, attenuate

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

import pandas as pd

roots = pd.read_excel("roots_df.xlsx")

cards = []
for row in roots.itertuples():
    cards.append(
        {
            "Front": f"What does the root '{row.root}' mean?",
            "Back": f"{row.meaning}\nExample words: {', '.join(row.example_words.split())}",
        }
    )


df = pd.DataFrame(cards)
df.to_csv(
    "anki_import_all_cards.txt", sep="\t", index=False, header=False, encoding="utf-8"
)
