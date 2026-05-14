import requests

API_KEY = "TVOJ_API_KLJUC"

url = "https://api.spoonacular.com/recipes/complexSearch"

params = {
    "apiKey": API_KEY,
    "type": "dessert",
    "number": 1000,          # koliko receptov želiš
    "addRecipeInformation": True
}

response = requests.get(url, params=params)
data = response.json()

for recipe in data["results"]:
    print("Ime:", recipe["title"])
    print("ID:", recipe["id"])
    print("Slika:", recipe["image"])

    # dodatne informacije (če so na voljo)
    if "readyInMinutes" in recipe:
        print("Čas:", recipe["readyInMinutes"], "min")

    print("-" * 40)