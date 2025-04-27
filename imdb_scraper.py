# imdb_scraper.py
# Scrapes the IMDb Top 250 movies and saves them into a text file.

import requests
from bs4 import BeautifulSoup

# URL for IMDb Top 250 Movies
IMDB_TOP_250_URL = "https://www.imdb.com/chart/top"

def fetch_imdb_top_250():
    """
    Fetch the IMDb Top 250 movies from the website.
    
    Returns:
        list: A list of movie titles.
    """
    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    response = requests.get(IMDB_TOP_250_URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from IMDb. Status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Select all 'a' tags inside 'td' with class 'titleColumn'
    movie_tags = soup.select('td.titleColumn a')
    
    imdb_top_250 = [tag.text.strip() for tag in movie_tags]
    return imdb_top_250


def save_movies_to_file(movies, filename):
    """
    Save a list of movie titles to a text file.
    
    Args:
        movies (list): List of movie titles.
        filename (str): Path to the output file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for movie in movies:
            file.write(f"{movie}\n")  # Write each movie on a new line

def main():
    """Main function to fetch and save IMDb Top 250 movies."""
    movies = fetch_imdb_top_250()  # Fetch the movies
    save_movies_to_file(movies, "lists/imdb_top_250.txt")  # Save the movies into a text file
    print(f"✅ Successfully saved {len(movies)} movies to 'lists/imdb_top_250.txt'!")  # Confirmation

if __name__ == "__main__":
    main()
