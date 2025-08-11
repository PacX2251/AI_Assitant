import requests

SCRAPI_API_URL = "http://localhost:1337/api/ai-conversations"  # cambia al URL real

def get_publication(publication_id):
    url = f"{SCRAPI_API_URL}/{publication_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching publication:", response.text)
        return None

# Ejemplo de uso
publication = get_publication("t2m7953t8vzt63vbkwyr0qj2")
print(publication)