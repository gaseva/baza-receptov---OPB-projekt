import string
import requests
import pandas as pd

all_desserts = []

API_KEY = "d35fcc08c9a14675876a51cd5e40706f"
url = "https://api.spoonacular.com/recipes/complexSearch"
params = {
    "apiKey": API_KEY,
}

response = requests.get(url, params=params)

data = response.json()

for recipe in data["results"]:
    all_desserts.append(recipe)


# Pretvori v DataFrame
df = pd.DataFrame(all_desserts)

# Shrani v CSV
df.to_csv("C:\\Users\\uporabnik\\Documents\\1_faks\\OPB\\projekt\\baza-receptov---OPB-projekt\\data\\podatki.csv", index=False, encoding="utf-8")

print("CSV shranjen!")