# scripts/merge_movies.py
import json
import os

def load_movies(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_movies(movies, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

def unique_movies(movies):
    seen = set()
    unique = []
    for movie in movies:
        key = (movie['title'].lower(), movie['year'])  # lowercase title + year
        if key not in seen:
            seen.add(key)
            unique.append(movie)
    return unique

if __name__ == "__main__":
    sources = [
        'lists/imdb_top_250_updated_standardized.json',
        'lists/afi_top_100_updated_standardized.json',
        'lists/letterboxd_top_250_updated_standardized.json',
        # Add more if you want
    ]

    all_movies = []
    for source in sources:
        movies = load_movies(source)
        all_movies.extend(movies)

    all_movies = unique_movies(all_movies)
