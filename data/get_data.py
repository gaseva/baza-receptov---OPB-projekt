import string
import requests


all_desserts = []

for letter in string.ascii_lowercase:
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"
    response = requests.get(url)
    data = response.json()

    if data["meals"]:
        for meal in data["meals"]:
            # FILTRIRANJE NA SLADICE
            if meal["strCategory"] == "Dessert":
                all_desserts.append(meal)

print(all_desserts)
