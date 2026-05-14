import string
import requests
import pandas as pd

all_desserts = []

for letter in string.ascii_lowercase:
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"
    response = requests.get(url)
    data = response.json()

    if data["meals"]:
        for meal in data["meals"]:
            if meal["strCategory"] == "Dessert":
                all_desserts.append(meal)

# Pretvori v DataFrame
df = pd.DataFrame(all_desserts)

# Shrani v CSV
df.to_csv("C:\\Users\\uporabnik\\Documents\\1_faks\\OPB\\projekt\\baza-receptov---OPB-projekt\\data\\podatki.csv", index=False, encoding="utf-8")

print("CSV shranjen!")


