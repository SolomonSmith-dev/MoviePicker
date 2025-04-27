# scripts/fill_missing_data.py
import json
import requests
import time

OMDB_API_KEY = "e130a52d"
OMDB_API_URL = "http://www.omdbapi.com/"

def load_movies(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_movies(movies, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

def fetch_movie_data(title):
    """Fetch movie details from OMDb API."""
    params = {
        't': title,
        'apikey': OMDB_API_KEY
    }
    try:
        response = requests.get(OMDB_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return {
                    'year': data.get('Year', ''),
                    'director': data.get('Director', ''),
                    'genres': data.get('Genre', '')
                }
            else:
                print(f"❌ Not found on OMDb: {title}")
                return None
        else:
            print(f"❌ Error fetching {title}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Exception fetching {title}: {e}")
        return None

def update_movie(movie):
    """Update movie info if missing."""
    if (movie['year'].lower() == 'unknown' or
        movie['director'].lower() == 'unknown' or
        movie['genres'].lower() == 'unknown' or
        not movie['year'] or
        not movie['director'] or
        not movie['genres']):
        
        data = fetch_movie_data(movie['title'])
        if data:
            if not movie.get('year') or movie['year'].lower() == 'unknown':
                movie['year'] = data['year']
            if not movie.get('director') or movie['director'].lower() == 'unknown':
                movie['director'] = data['director']
            if not movie.get('genres') or movie['genres'].lower() == 'unknown':
                movie['genres'] = data['genres']
        time.sleep(0.5)  # Be gentle with API to avoid getting rate limited

    return movie

if __name__ == "__main__":
    filepath = 'lists/standardized_movies.json'
    movies = load_movies(filepath)

    print(f"🔎 Found {len(movies)} movies. Filling missing data...")

    updated_movies = []
    seen = set()

    for movie in movies:
        key = (movie['title'].lower(), movie.get('year', '').lower())
        if key not in seen:
            updated_movie = update_movie(movie)
            updated_movies.append(updated_movie)
            seen.add(key)
        else:
            print(f"⚠️ Duplicate skipped: {movie['title']}")

    save_movies(updated_movies, filepath)

    print(f"✅ Done! Saved {len(updated_movies)} clean movies.")
