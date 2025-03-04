import os
import requests
import json
from github import Github

# Obtener el token de la API de Noticias desde el secreto
API_KEY = os.getenv("API_NEWS")

# Realizar la solicitud a la API de noticias
def get_news():
    url = f'https://newsapi.org/v2/top-headlines?country=ve&language=es&apiKey={API_KEY}'
    response = requests.get(url)
    news = response.json()

    # Verificar si la solicitud fue exitosa
    if news['status'] == 'ok':
        # Extrae los titulares de las noticias
        headlines = [article['title'] for article in news['articles'][:5]]
        return headlines
    else:
        print("Error al obtener noticias:", news.get('message', 'Sin mensaje de error'))
        return []

# Crear archivo JSON
def save_to_json(data):
    with open("news_data.json", "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("Datos guardados correctamente en news_data.json")

# Subir el archivo JSON a GitHub
def upload_to_github():
    # Conectar con GitHub usando el token de GitHub
    github_token = os.getenv("GITHUB_TOKEN")
    g = Github(github_token)
    repo = g.get_repo("baraltense/news")  # Cambia a tu usuario/repositorio

    with open("news_data.json", "r") as file:
        content = file.read()

    try:
        # Si el archivo existe, lo actualiza; si no, lo crea
        repo.create_file("news_data.json", "Subiendo noticias", content, branch="main", committer="GitHub Actions", author="GitHub Actions")
        print("Archivo subido correctamente a GitHub.")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")

# Llamada a la función
if __name__ == "__main__":
    headlines = get_news()
    if headlines:
        save_to_json(headlines)
        upload_to_github()
    else:
        print("No se pudieron obtener titulares de noticias.")
