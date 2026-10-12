import pandas as pd

# 1. Lire et garder les données utiles
df = pd.read_excel("data/raw/Tourisme-PF-2025.xlsx", header=None, skiprows=4)
df = df.iloc[:, :5]
df.columns = ["libelle", "2019", "2023", "2024", "2025"]
df = df.dropna(subset=["libelle"])
df["libelle"] = df["libelle"].str.strip()
df = df[df["libelle"] != "Total"]

# 2. Repérer le mode de transport de chaque ligne
modes = {"T.AIR": "Aérien", "T.MER": "Maritime", "T.TERRE": "Terrestre"}
df["mode_transport"] = df["libelle"].map(modes).ffill()
df["est_sous_total"] = df["libelle"].isin(modes.keys())

# 3. Nettoyer le nom du point d'entrée (retirer les préfixes "A " et "T ")
df["point_entree"] = df["libelle"].str.replace(r"^(A|T) ", "", regex=True)

# 4. Format long
df_long = df.melt(
    id_vars=["mode_transport", "est_sous_total", "point_entree"],
    value_vars=["2019", "2023", "2024", "2025"],
    var_name="annee", value_name="arrivees",
)
df_long["annee"] = df_long["annee"].astype(int)
df_long["arrivees"] = df_long["arrivees"].astype(int)

# 5. Séparer les sous-totaux du détail
sous_totaux = df_long[df_long["est_sous_total"]]
detail = df_long[~df_long["est_sous_total"]]

# 6. Calculer l'écart (sous-total - détail) pour chaque mode et année
somme_detail = detail.groupby(["mode_transport", "annee"])["arrivees"].sum()
valeur_st = sous_totaux.groupby(["mode_transport", "annee"])["arrivees"].sum()
ecart = (valeur_st - somme_detail).reset_index(name="arrivees")

# 7. Créer les lignes "Autres points" avec cet écart
autres = ecart.copy()
autres["point_entree"] = "Autres points - " + autres["mode_transport"]
autres["est_sous_total"] = False

# 8. Table finale : détail + "Autres points" (sans les sous-totaux)
fact = pd.concat([detail, autres[detail.columns]], ignore_index=True)
fact = fact.drop(columns="est_sous_total")
fact = fact.sort_values(["annee", "mode_transport", "point_entree"]).reset_index(drop=True)

# 9. Sauvegarder
fact.to_csv("data/clean/fact_point_entree.csv", index=False, encoding="utf-8-sig")

# 10. Contrôle qualité : on doit retrouver les totaux officiels
attendus = {2019: 12932734, 2023: 14524727, 2024: 17411949, 2025: 19792594}
totaux = fact.groupby("annee")["arrivees"].sum()
print(fact.head(10))
print("Lignes x colonnes :", fact.shape)
print()
for annee, attendu in attendus.items():
    ok = totaux[annee] == attendu
    print(annee, totaux[annee], "OK" if ok else "ERREUR")