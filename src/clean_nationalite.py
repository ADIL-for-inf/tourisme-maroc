import pandas as pd

# 1. Lire et garder les données utiles (comme avant)
df = pd.read_excel("data/raw/Evolution_nationalite_PF-2025.xlsx",
                   header=None, skiprows=4)
df = df.iloc[:, :5]
df.columns = ["pays", "2019", "2023", "2024", "2025"]
df = df.dropna(subset=["pays"])
df["pays"] = df["pays"].str.strip()
df = df[df["pays"] != "Total"]

# 2. Passer au format long : une ligne par pays et par année
df_long = df.melt(id_vars="pays", var_name="annee", value_name="arrivees")

# 3. Corriger les types (nombres entiers)
df_long["annee"] = df_long["annee"].astype(int)
df_long["arrivees"] = df_long["arrivees"].astype(int)

# 4. Harmoniser les noms de pays
df_long["pays"] = df_long["pays"].replace({
    "Hollande": "Pays-Bas",
    "Etats Unis": "États-Unis",
})

# 5. Sauvegarder la table propre
df_long.to_csv("data/clean/fact_nationalite.csv", index=False, encoding="utf-8-sig")

# 6. Vérifications
print(df_long.head(10))
print("Lignes x colonnes :", df_long.shape)
print("Total arrivées 2025 :", df_long[df_long["annee"] == 2025]["arrivees"].sum())