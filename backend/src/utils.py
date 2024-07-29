import os
import requests
from dotenv import load_dotenv
from datetime import date

load_dotenv()

key = os.getenv("RESCUE_GROUPS_API_KEY")

request_fields = {
    "apikey": key,
    "objectType": "animals",
    "objectAction": "publicSearch",
    "search":
    {
        "resultStart": "0",
        "resultLimit": "10",
        "resultSort": "animalName",
        "resultOrder": "asc",
        "filters":
        [
            {
                "fieldName": "animalSpecies",
                "operation": "equals",
                "criteria": "Dog"
                 
            }
        ],
        "filterProcessing": "1",
        "fields": ["animalName","animalSpecies","animalBreed","animalBirthdate", "animalSex", "animalLocation", "animalPlayful", "animalPictures"]
    }
}

rescue_groups_url = "https://api.rescuegroups.org/http/v2.json"

response = requests.post(rescue_groups_url, json=request_fields)
data = response.json()['data']

def calc_age(year, month, day):
    today = date.today()
    return today.year - int(year) - ((today.month, today.day) < (int(month), int(day)))

url = "http://127.0.0.1:8000/api/pets/"

for key in data:
    entry = data[key]

    birthdate = entry['animalBirthdate'].split('/')
    age = calc_age(birthdate[2], birthdate[0], birthdate[1])

    body = {
        "name": entry['animalName'],
        "species": entry['animalSpecies'],
        "breed": entry['animalBreed'],
        "age": age,
        "gender": entry['animalSex'],
        "location": entry['animalLocation'],
        "description": entry['animalPlayful'],
        "photo_url": entry["animalPictures"]["urlSecureFullsize"],
        "shelter_id": 13
    }

    response = requests.post(url, json=body)