import json
import random
import os

# Where your beautified files are stored
LISTS_FOLDER = "lists"

def load_movies():
    """Load all beautified movie lists into one master list."""
    all_movies = []
    filenames = [
        "imdb_top_250_beautified.json",
        "afi_top_100_beautified.json",
        "letterboxd_top_250_beautified.json"
    ]
    for filename in filenames:
        path = os.path.join(LISTS_FOLDER, filename)
        try:
            with open(path, "r", encoding="utf-8") as file:
                movies = json.load(file)
                all_movies.extend(movies)
        except Exception as e:
            print(f"⚠️ Error loading {filename}: {e}")
    return all_movies

def search_by_year(movies, year):
    return [movie for movie in movies if str(year) in movie.get("year", "")]

def search_by_director(movies, director_name):
    return [movie for movie in movies if director_name.lower() in movie.get("director", "").lower()]

def search_by_genre(movies, genre):
    return [movie for movie in movies if genre.lower() in movie.get("genres", "").lower()]

def search_by_title(movies, title):
    return [movie for movie in movies if title.lower() in movie.get("title", "").lower()]

def random_movie(movies):
    return random.choice(movies) if movies else None

def main():
    movies = load_movies()
    if not movies:
        print("❌ No movies loaded. Check your JSON files!")
        return

    print("🎬 Welcome to QuickChecker!")
    print("------------------------------")

    while True:
        print("\nChoose an option:")
        print("1. Search by Year")
        print("2. Search by Director")
        print("3. Search by Genre")
        print("4. Search by Title")
        print("5. Pick Random Movie 🎲")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            year = input("Enter a year (e.g., 1994): ")
            results = search_by_year(movies, year)
        elif choice == "2":
            director = input("Enter a director's name (e.g., Christopher Nolan): ")
            results = search_by_director(movies, director)
        elif choice == "3":
            genre = input("Enter a genre (e.g., Drama, Comedy, Action): ")
            results = search_by_genre(movies, genre)
        elif choice == "4":
            title = input("Enter a movie title keyword: ")
            results = search_by_title(movies, title)
        elif choice == "5":
            movie = random_movie(movies)
            if movie:
                print(f"\n🎲 Random Movie: {movie.get('title', 'Unknown Title')} ({movie.get('year', 'Unknown Year')})")
            else:
                print("\n❌ No movies found!")
            continue
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Try again.")
            continue

        if results:
            print(f"\n✅ Found {len(results)} movies:")
            for movie in results:
                print(f"- {movie.get('title', 'Unknown Title')} ({movie.get('year', 'Unknown Year')})")
        else:
            print("\n❌ No results found.")

if __name__ == "__main__":
    main()
