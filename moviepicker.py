
import json
import random
import datetime
from colorama import Fore, Style, init
init(autoreset=True)

def load_movies(filepath):
    """Load the movie list from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def fallback(value, field_name):
    """Fallback for missing fields."""
    if not value or value.lower() == 'unknown':
        if field_name == 'director':
            return 'Unknown Director'
        elif field_name == 'year':
            return 'Unknown Year'
        elif field_name == 'genres':
            return 'Unknown Genres'
    return value

def pick_random_movie(movies):
    """Pick and return a random movie from the list."""
    if not movies:
        return None
    return random.choice(movies)

def pick_movie_by_genres(movies, desired_genres):
    """Pick a random movie that matches ALL desired genres first, then fallback to ANY."""
    # First: strict AND matching
    strict_matches = []
    for movie in movies:
        movie_genres = [g.strip().lower() for g in fallback(movie.get('genres', ''), 'genres').split(',')]
        if all(genre.lower() in movie_genres for genre in desired_genres):
            strict_matches.append(movie)

    if strict_matches:
        print(f"\n✅ Found a perfect match!")
        return random.choice(strict_matches)

    # If no strict matches: fallback to OR matching
    print("\n⚠️ No perfect match found. Trying partial matches...")
    loose_matches = []
    for movie in movies:
        movie_genres = [g.strip().lower() for g in fallback(movie.get('genres', ''), 'genres').split(',')]
        if any(genre.lower() in movie_genres for genre in desired_genres):
            loose_matches.append(movie)

    if loose_matches:
        return random.choice(loose_matches)
    else:
        return None

def show_movie(movie, header="Movie Picked!"):
    """Display movie details cleanly and professionally."""
    if not movie:
        print("\n❌ No movie to display.")
        return

    title = fallback(movie.get('title', 'Unknown Title'), 'title')
    director = fallback(movie.get('director', ''), 'director')
    year = fallback(movie.get('year', ''), 'year')
    genres = fallback(movie.get('genres', ''), 'genres')

    print("\n" + "━" * 60)
    print(f"🎬 {Fore.CYAN}{Style.BRIGHT}{header}{Style.RESET_ALL}")
    print("━" * 60)
    print(f"🎞️  {Fore.BLUE}Title    :{Style.RESET_ALL} {title}")
    print(f"🎬 {Fore.YELLOW}Director :{Style.RESET_ALL} {director}")
    print(f"📅 {Fore.GREEN}Year     :{Style.RESET_ALL} {year}")
    print(f"🎭 {Fore.MAGENTA}Genres   :{Style.RESET_ALL} {genres}")
    print("━" * 60)
    print()  # Blank line after movie


def pick_movie_of_the_day(movies):
    """Pick a movie of the day based on today's date."""
    today = datetime.date.today()
    random.seed(today.toordinal())  # Use the date to create a fixed seed
    return random.choice(movies)

def main():
    greatest_movies = load_movies('lists/standardized_movies_final.json')
    plex_movies = load_movies('lists/plex_movies_final.json')
    combined_movies = greatest_movies + plex_movies

    print("\n")  # <<--- NEW: Add a blank line 
    print("🎥 Welcome to Movie Picker!\n")

    # Show Movie of the Day
    movie_of_the_day = pick_movie_of_the_day(combined_movies)
    show_movie(movie_of_the_day, header="Movie of the Day")

    pick_today = input("🎬 Would you like to watch the Movie of the Day? (y/n): ")
    if pick_today.lower() == 'y':
        print("\n🎉 Enjoy your Movie of the Day! Goodbye!\n")
        return  # End the program after picking Movie of the Day

    while True:
        print("1. Pick from Greatest Movies")
        print("2. Pick from My Plex Movies")
        print("3. Pick a Movie by Genre (Combined List)")
        choice = input("\nChoose an option (1, 2, or 3): ")

        if choice == '1':
            movie = pick_random_movie(greatest_movies)
            show_movie(movie)

        elif choice == '2':
            movie = pick_random_movie(plex_movies)
            show_movie(movie)

        elif choice == '3':
            user_input = input("\n🎬 What genres are you feeling? (comma-separated, e.g., 'Animation, Adventure')\n> ")
            desired_genres = [g.strip() for g in user_input.split(',')]
            movie = pick_movie_by_genres(combined_movies, desired_genres)
            show_movie(movie)

        else:
            print("\n❌ Invalid choice.")

        again = input("🔁 Pick another movie? (y/n): ")
        if again.lower() != 'y':
            print("\n👋 Goodbye! Enjoy your movie!")
            break
        print()

if __name__ == "__main__":
    main()

