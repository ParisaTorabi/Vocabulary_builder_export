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

if __name__ == "__main__":
    roots = pd.read_excel("roots_df.xlsx")

    cards = []
    for row in roots.itertuples():
        cards.append(
            {
                "Front": f"What does the root '{row.root}' mean?",
                "Back": f"{row.meaning}\nExample words: {', '.join(row.example_words.split())}",
            }
        )

    words = pd.read_excel("words_df.xlsx", header=0, index_col=0)

    for row in words.itertuples():
        cards.append(
            {
                "Front": f"What does the word '{row.word.strip()}' mean?",
                "Back": f"{row.definition}",
            }
        )
        cards.append(
            {
                "Front": f"What is the root of '{row.word.strip()}'?",
                "Back": f"{row.root}",
            }
        )

        cards.append(
            {
                "Front": row.sentence.replace(row.word.strip(), "---"),
                "Back": f"{row.word.strip()}",
            }
        )

    # check if all the cards are added. 259+1200*3 = 3859
    if len(cards) == 3859:
        print("All cards successfully added.")

    df = pd.DataFrame(cards)
    df.to_csv(
        "anki_import_all_cards.txt",
        sep="\t",
        index=False,
        header=False,
        encoding="utf-8",
    )
