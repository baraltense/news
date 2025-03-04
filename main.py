import os
import requests
from github import Github

# Obtener el token de la API de Noticias desde el secreto
API_KEY = os.getenv("API_NEWS")

# Realizar la solicitud a la API de noticias
def get_news():
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'
    response = requests.get(url)
    news = response.json()

    # Extrae los titulares de las noticias
    headlines = [article['title'] for article in news['articles'][:5]]
    return headlines

# Crear archivo JSON
def save_to_json(data):
    with open("news_data.json", "w") as file:
        json.dump(data, file)
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
        repo.create_file("news_data.json", "Subiendo noticias", content, branch="main")
        print("Archivo subido correctamente a GitHub.")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")

# Llamada a la función
if __name__ == "__main__":
    headlines = get_news()
    save_to_json(headlines)
    upload_to_github()
