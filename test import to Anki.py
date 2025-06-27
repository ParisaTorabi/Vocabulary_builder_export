import pandas as pd

data = [
    {
        "Front": "What does 'benevolent' mean?",
        "Back": "Kind and generous \n(bene = good)",
    },
    {"Front": "Root of 'benefactor'?", "Back": "bene = good"},
]

df = pd.DataFrame(data)
df.to_csv("anki_import.txt", sep="\t", index=False, header=False, encoding="utf-8")
