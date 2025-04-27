# moviepicker.py
import json
import random

def load_movies(filepath):
    """Load the movie list from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading movies: {e}")
        return []

def pick_random_movie(movies):
    """Pick and return a random movie from the list."""
    if not movies:
        return None
    return random.choice(movies)

def show_movie(movie):
    """Display the movie details nicely."""
    if movie:
        print("\n🎬 Your Random Movie Pick:")
        print(f"Title    : {movie['title']}")
        print(f"Year     : {movie['year']}")
        print(f"Director : {movie['director']}")
        print(f"Genres   : {movie['genres']}\n")
    else:
        print("No movies found to pick from!")

if __name__ == "__main__":
    movies = load_movies('lists/standardized_movies.json')
    movie = pick_random_movie(movies)
    show_movie(movie)
