
import json

def load_movies(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_movies(movies, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

def fix_directors(movies):
    for movie in movies:
        director = movie.get('director', 'Unknown Director')
        if director.lower() == 'unknown director':
            title = movie.get('title', 'Unknown Title')
            year = movie.get('year', 'Unknown Year')
            print(f"\n🎬 Title: {title} ({year})")
            print(f"Current Director: {director}")
            new_director = input("Enter the correct director (or press Enter to skip): ").strip()
            if new_director:
                movie['director'] = new_director
    return movies

if __name__ == "__main__":
    plex_movies_path = 'lists/plex_movies_final.json'
    fixed_movies_path = 'lists/plex_movies_fixed.json'

    movies = load_movies(plex_movies_path)
    print(f"🔎 Found {len(movies)} Plex movies.")
    print("🎯 Starting manual director fixer...")

    updated_movies = fix_directors(movies)
    save_movies(updated_movies, fixed_movies_path)

    print(f"✅ Done! Saved fixed Plex movies to {fixed_movies_path}.")
