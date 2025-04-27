
import json
import os

def load_movies(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_movies(movies, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

def fix_directors(movies):
    unknown_director_movies = [m for m in movies if m.get('director', '').lower() == 'unknown director']
    print(f"🎯 {len(unknown_director_movies)} movies need fixing (Unknown Director).")

    for movie in movies:
        director = movie.get('director', 'Unknown Director')
        if director.lower() == 'unknown director':
            title = movie.get('title', 'Unknown Title')
            year = movie.get('year', 'Unknown Year')
            print(f"\n🎬 Title: {title} ({year})")
            print(f"Current Director: {director}")
            new_director = input("Enter the correct director (press Enter to skip, 'q' to quit): ").strip()

            if new_director.lower() == 'q':
                print("\n💾 Saving progress and quitting...")
                return movies  # Save and quit immediately

            if new_director:
                movie['director'] = new_director

    return movies

if __name__ == "__main__":
    original_path = 'lists/plex_movies_final.json'
    fixed_path = 'lists/plex_movies_fixed.json'

    if os.path.exists(fixed_path):
        print("🔎 Found existing fixed file. Resuming progress...")
        movies = load_movies(fixed_path)
    else:
        print("🔎 No fixed file found. Starting fresh...")
        movies = load_movies(original_path)

    updated_movies = fix_directors(movies)
    save_movies(updated_movies, fixed_path)

    print(f"✅ Done! Saved fixed Plex movies to {fixed_path}.")
