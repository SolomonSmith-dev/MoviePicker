# scripts/pull_plex_movies.py

import requests
import xml.etree.ElementTree as ET
import json

# Plex server settings
PLEX_SERVER_URL = "http://192.168.1.177:32400"
PLEX_TOKEN = "DxXyAsQ1i537xuM2Vbe2"

def fetch_movies():
    headers = {
        "Accept": "application/xml",
        "X-Plex-Token": PLEX_TOKEN
    }
    url = f"{PLEX_SERVER_URL}/library/sections/1/all?type=1"  # 'type=1' = movies

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error connecting to Plex Server: {response.status_code}")
        return []

    movies = []
    root = ET.fromstring(response.content)

    for video in root.findall(".//Video"):
        title = video.attrib.get('title', 'Unknown Title')
        year = video.attrib.get('year', 'Unknown Year')
        director = video.attrib.get('director', 'Unknown Director')
        genres = [genre.attrib['tag'] for genre in video.findall('.//Genre')]
        genres_str = ", ".join(genres) if genres else 'Unknown'

        movies.append({
            'title': title,
            'year': year,
            'director': director,
            'genres': genres_str
        })

    return movies

def save_movies(movies, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    print("📡 Connecting to Plex Server...")
    movies = fetch_movies()
    if movies:
        save_movies(movies, 'lists/plex_movies.json')
        print(f"✅ Saved {len(movies)} movies to lists/plex_movies.json!")
    else:
        print("❌ No movies found or error pulling data.")
