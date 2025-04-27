# scripts/clean_plex_movies.py

import json
import requests
import time

# Plex OMDb API Key
OMDB_API_KEY = "e130a52d"
OMDB_API_URL = "http://www.omdbapi.com/"

def load_movies(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_movies(movies, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

def clean_title(title):
    """Remove extra tags like 'Remastered', 'Criterion Collection', etc."""
    bad_words = [
        'Criterion Collection', 'Remastered', 'Theatrical Edition', 
        'Open Matte', 'Uncut', "Director's Cut", "Extended Cut"
    ]
    for bad_word in bad_words:
        title = title.replace(bad_word, '')
    return title.strip()

def fetch_movie_data(title):
    """Fetch movie details from OMDb API."""
    cleaned_title = clean_title(title)
    params = {
        't': cleaned_title,
        'apikey': OMDB_API_KEY
    }
    try:
        response = requests.get(OMDB_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                print(f"✅ Found and updated: {cleaned_title}")
                return {
                    'year': data.get('Year', ''),
                    'director': data.get('Director', ''),
                    'genres': data.get('Genre', '')
                }
            else:
                print(f"❌ Not found on OMDb: {cleaned_title} (original: {title})")
                return None
        else:
            print(f"❌ Error fetching {cleaned_title}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Exception fetching {cleaned_title}: {e}")
        return None

def update_movie(movie):
    """Update movie info if missing."""
    if (movie.get('year', '').lower() == 'unknown' or
        movie.get('director', '').lower() == 'unknown' or
        movie.get('genres', '').lower() == 'unknown' or
        not movie.get('year') or
        not movie.get('director') or
        not movie.get('genres')):
        
        data = fetch_movie_data(movie['title'])
        if data:
            if not movie.get('year') or movie['year'].lower() == 'unknown':
                movie['year'] = data['year']
            if not movie.get('director') or movie['director'].lower() == 'unknown':
                movie['director'] = data['director']
            if not movie.get('genres') or movie['genres'].lower() == 'unknown':
                movie['genres'] = data['genres']
        time.sleep(0.5)  # Be nice to OMDb API
    return movie

def remove_duplicates(movies):
    seen = set()
    unique = []
    for movie in movies:
        key = (movie['title'].lower(), movie.get('year', '').lower())
        if key not in seen:
            seen.add(key)
            unique.append(movie)
    return unique

if __name__ == "__main__":
    filepath = 'lists/plex_movies.json'
    movies = load_movies(filepath)

    print(f"🔎 Found {len(movies)} Plex movies. Cleaning...")

    updated_movies = []
    for movie in movies:
        updated_movie = update_movie(movie)
        updated_movies.append(updated_movie)

    updated_movies = remove_duplicates(updated_movies)

    save_movies(updated_movies, 'lists/plex_movies_cleaned.json')

    print(f"✅ Done! Saved {len(updated_movies)} cleaned Plex movies to 'lists/plex_movies_cleaned.json'.")
