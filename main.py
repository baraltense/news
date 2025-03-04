import os
import requests
import json
from github import Github

# Obtener el token de la API de noticias desde el secreto NEWS_API_KEY
API_KEY = os.getenv("NEWS_API_KEY")

# URL base de la nueva API (NewsDataHub)
BASE_URL = 'https://api.newsdatahub.com/v1/news'

# Encabezados para la API
headers = {
    'X-Api-Key': API_KEY,
    'User-Agent': 'YourApp/1.0'  # Reemplaza "YourApp/1.0" con el nombre de tu aplicación si lo deseas
}

# Función para obtener noticias internacionales en español
def get_news():
    # Usamos el parámetro language=es para obtener artículos en español
    params = {'language': 'es'}
    response = requests.get(BASE_URL, headers=headers, params=params)
    news = response.json()
    
    if 'data' in news:
        # Extraemos los primeros 5 titulares
        headlines = [article['title'] for article in news['data'][:5]]
        return headlines
    else:
        print("Error al obtener noticias:", news.get('message', 'Sin mensaje de error'))
        return []

# Función para guardar los titulares en un archivo JSON
def save_to_json(data):
    with open("news_data.json", "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("Datos guardados correctamente en news_data.json")

# Función para subir el archivo JSON a GitHub
def upload_to_github():
    # Conectar con GitHub usando el token almacenado en el secreto API_NEW
    github_token = os.getenv("API_NEW")
    g = Github(github_token)
    repo = g.get_repo("baraltense/news")  # Asegúrate de que el repositorio sea correcto

    with open("news_data.json", "r", encoding='utf-8') as file:
        content = file.read()

    try:
        # Intentamos crear el archivo en la rama "main"
        repo.create_file("news_data.json", "Subiendo noticias internacionales en español", content, branch="main")
        print("Archivo subido correctamente a GitHub.")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")

# Ejecución principal del script
if __name__ == "__main__":
    headlines = get_news()
    if headlines:
        save_to_json(headlines)
        upload_to_github()
    else:
        print("No se pudieron obtener titulares de noticias.")
