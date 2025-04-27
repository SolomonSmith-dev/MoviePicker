import requests
import json
import os

def fetch_letterboxd_top_250():
    """
    Fetch the Letterboxd Top 250 Narrative Films list from a free API.
    
    Returns:
        list: A list of movie dictionaries.
    """
    url = "https://letterboxd-list-radarr.onrender.com/dave/list/official-top-250-narrative-feature-films/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Letterboxd Top 250 list. Status code: {response.status_code}")

    return response.json()

def save_movies_to_file(movies, filename):
    """
    Save a list of movies to a JSON file.
    
    Args:
        movies (list): List of movie data (dicts).
        filename (str): Path to the output file.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(movies, file, ensure_ascii=False, indent=2)

def main():
    """Main function to fetch and save Letterboxd Top 250 movies."""
    print("🔎 Fetching Letterboxd Top 250...")
    movies = fetch_letterboxd_top_250()
    save_movies_to_file(movies, "lists/letterboxd_top_250_raw.json")
    print(f"✅ Successfully saved {len(movies)} movies to 'lists/letterboxd_top_250_raw.json'!")

if __name__ == "__main__":
    main()
