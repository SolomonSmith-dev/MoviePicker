import json
import os

# Where your beautified files are stored
LISTS_FOLDER = "lists"

# Function to load all beautified movie lists into one master list
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

# Function to prompt the user to update missing data
def update_missing_data(movie):
    """Prompt the user for missing data and update the movie."""
    updated = False

    # Check if title is missing
    if not movie.get("title"):
        movie["title"] = input("Enter the title of the movie: ")
        updated = True

    # Check if year is missing
    if not movie.get("year"):
        movie["year"] = input(f"Enter the year of the movie '{movie['title']}': ")
        updated = True

    # Check if director is missing
    if not movie.get("director"):
        movie["director"] = input(f"Enter the director(s) of the movie '{movie['title']}': ")
        updated = True

    # Check if genres are missing
    if not movie.get("genres"):
        movie["genres"] = input(f"Enter the genres of the movie '{movie['title']}': ")
        updated = True

    return updated

# Function to save the updated movie list back to JSON file
def save_updated_movies(movies, filename):
    """Save the updated movies to the JSON file."""
    path = os.path.join(LISTS_FOLDER, filename)
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(movies, file, indent=4, ensure_ascii=False)
        print(f"✅ Updated movies saved to '{filename}'!")
    except Exception as e:
        print(f"⚠️ Error saving the updated file: {e}")

# Main function to update missing data in movies
def main():
    # Load all movies
    movies = load_movies()

    if not movies:
        print("❌ No movies found. Please check your JSON files.")
        return

    print("🎬 Updating missing movie data...")

    updated_count = 0
    for movie in movies:
        if update_missing_data(movie):
            updated_count += 1

    if updated_count > 0:
        print(f"\n✅ Successfully updated {updated_count} movies.")
        save_updated_movies(movies, "updated_movies.json")
    else:
        print("\n❌ No missing data found in the movies.")

if __name__ == "__main__":
    main()
