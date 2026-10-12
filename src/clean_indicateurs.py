import pandas as pd

# 1. Lire toute la feuille brute
raw = pd.read_excel("data/raw/Indicateurs-touristiques-2025.xlsx",
                    sheet_name="Graphes", header=None)

# 2. Mots-clés des titres -> nom de la colonne finale
titres = {
    "Arrivées": "arrivees",
    "Nuitées": "nuitees",
    "Recettes": "recettes_mdh",
}

# 3. Parcourir les lignes
bloc = None
lignes = []
for _, r in raw.iterrows():
    c0, c1 = r[0], r[1]
    annee = pd.to_numeric(c0, errors="coerce")   # "2019" ou 2019 -> 2019 ; un titre -> NaN
    if pd.isna(annee):
        if isinstance(c0, str):                  # c'est un titre de tableau
            for mot, nom in titres.items():
                if mot in c0:
                    bloc = nom
        continue
    if pd.notna(c1) and bloc:                    # ligne année + valeur
        lignes.append((int(annee), bloc, float(c1)))

long = pd.DataFrame(lignes, columns=["annee", "indicateur", "valeur"])

# 4. Une ligne par année, une colonne par indicateur
df = (long.pivot(index="annee", columns="indicateur", values="valeur")
          .reset_index()
          .rename_axis(columns=None))

# 5. Types
df["arrivees"] = df["arrivees"].astype("Int64")
df["nuitees"] = df["nuitees"].astype("Int64")

# 6. Sauvegarder
df.to_csv("data/clean/fact_indicateurs_annuels.csv", index=False, encoding="utf-8-sig")

# 7. Vérifications
print(df)
print("Lignes x colonnes :", df.shape)
print("Années avec recettes :", df["recettes_mdh"].notna().sum())
print("Nuitées manquantes :", df["nuitees"].isna().sum())