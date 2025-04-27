import requests
from bs4 import BeautifulSoup
import json

AFI_URL = "https://en.wikipedia.org/wiki/AFI%27s_100_Years...100_Movies"

def fetch_afi_top_100():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    response = requests.get(AFI_URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch AFI list. Status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first wikitable
    table = soup.find('table', {'class': 'wikitable'})

    movies = []
    rows = table.find_all('tr')[1:]  # skip header row

    for idx, row in enumerate(rows, start=1):
        cells = row.find_all('td')
        if len(cells) >= 2:
            title = cells[0].get_text(strip=True)
            year = cells[1].get_text(strip=True)
            movies.append({
                "rank": idx,
                "title": title,
                "year": int(year)
            })

    return movies

def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    afi_movies = fetch_afi_top_100()
    save_to_json(afi_movies, "lists/afi_top_100_raw.json")
    print(f"✅ Successfully saved {len(afi_movies)} movies to 'lists/afi_top_100_raw.json'!")

if __name__ == "__main__":
    main()
