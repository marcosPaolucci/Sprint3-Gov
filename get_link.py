link = "https://raw.githubusercontent.com/giuliano-macedo/geodata-br-states/refs/heads/main/geojson/br_states.json"

#pegar json do link e salvar neste diretorio
import requests
import json

def download_geojson():
    response = requests.get(link)
    if response.status_code == 200:
        with open("br_states.json", "w") as f:
            json.dump(response.json(), f)
    else:
        print("Erro ao baixar o arquivo.")
        print(f"Status code: {response.status_code}")

download_geojson()