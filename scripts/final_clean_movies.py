
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

def clean_title(title):
    bad_words = [
        'Criterion Collection', 'Remastered', 'Theatrical Edition',
        'Open Matte', 'Uncut', "Director's Cut", "Extended Cut"
    ]
    for bad_word in bad_words:
        title = title.replace(bad_word, '')
    return title.strip()

def fetch_movie_data(title):
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
                return {
                    'year': data.get('Year', ''),
                    'director': data.get('Director', ''),
                    'genres': data.get('Genre', '')
                }
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"❌ Exception fetching {cleaned_title}: {e}")
        return None

def fallback(value, field_name):
    if not value or value.lower() == 'unknown':
        if field_name == 'director':
            return 'Unknown Director'
        elif field_name == 'year':
            return 'Unknown Year'
        elif field_name == 'genres':
            return 'Unknown Genres'
    return value

def update_movie(movie):
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
        time.sleep(0.5)  # Respect OMDb API limits

    # Apply fallback values
    movie['year'] = fallback(movie.get('year', ''), 'year')
    movie['director'] = fallback(movie.get('director', ''), 'director')
    movie['genres'] = fallback(movie.get('genres', ''), 'genres')

    return movie

def clean_file(input_path, output_path):
    movies = load_movies(input_path)
    print(f"🔎 Cleaning {len(movies)} movies from {input_path}...")
    cleaned = []
    for movie in movies:
        cleaned.append(update_movie(movie))
    save_movies(cleaned, output_path)
    print(f"✅ Saved {len(cleaned)} cleaned movies to {output_path}")

if __name__ == "__main__":
    clean_file('lists/standardized_movies.json', 'lists/standardized_movies_final.json')
    clean_file('lists/plex_movies_cleaned.json', 'lists/plex_movies_final.json')
