import requests
import json
import os
from github import Github

# Obtiene tu News API Key desde las variables de entorno (para proteger la clave)
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# URL de la API de NewsAPI
url = f'https://newsapi.org/v2/top-headlines?country=ve&apiKey={NEWS_API_KEY}'

# Realizar la consulta a la API
response = requests.get(url)
data = response.json()

# Verifica si la consulta fue exitosa
if response.status_code == 200:
    # Crear el archivo JSON con los datos obtenidos
    with open('news_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print("Datos guardados correctamente en news_data.json")
else:
    print("Error al obtener los datos de News API")

# Subir el archivo JSON a GitHub automáticamente (usa el token personal de GitHub)
def upload_to_github():
    # Autenticar con GitHub usando el token personal
    github_token = os.getenv('GITHUB_TOKEN')
    g = Github(github_token)
    repo = g.get_repo('baraltense/news')  # Reemplaza con tu usuario y repositorio
    
    # Abre el archivo JSON que se guardó
    with open("news_data.json", "rb") as file:
        content = file.read()

    # Subir el archivo a GitHub (asegúrate de que el archivo no exista previamente, o reemplázalo)
    repo.create_file("news_data.json", "Subiendo noticias", content, branch="main")
    print("Archivo JSON subido a GitHub.")

# Llamar a la función para subir el archivo
upload_to_github()
