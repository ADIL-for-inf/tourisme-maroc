import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

fichiers = [
    "data/raw/Evolution_nationalite_PF-2025.xlsx",
    "data/raw/Tourisme-PF-2025.xlsx",
    "data/raw/Indicateurs-touristiques-2025.xlsx",
]

for f in fichiers:
    xls = pd.ExcelFile(f)
    print("=" * 70)
    print(f, "-> feuilles :", xls.sheet_names)
    for feuille in xls.sheet_names:
        df = pd.read_excel(f, sheet_name=feuille, header=None)
        print(f"\n--- {feuille} : {df.shape[0]} lignes x {df.shape[1]} colonnes")
        print(df.head(12))