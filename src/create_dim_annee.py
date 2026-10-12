import pandas as pd

dim = pd.DataFrame({"annee": range(2013, 2026)})

def periode(a):
    if a < 2020:
        return "Avant Covid"
    if a <= 2021:
        return "Crise Covid-19"
    return "Reprise"

dim["periode"] = dim["annee"].apply(periode)

dim.to_csv("data/clean/dim_annee.csv", index=False, encoding="utf-8-sig")
print(dim)
print("Lignes x colonnes :", dim.shape)