import requests
import json
import time

API_KEY = 'YOUR KEY'
TOTAL_ARTICLES_NEEDED = 500
movies = [
    {"title": "Wicked", "keywords": ["Ariana Grande", "Jon M. Chu", "Cynthia Erivo", "Critics", "Cinema", "Box Office", "Glinda", "Elphaba", "Musical", "Stephen Schwartz", "Winnie Holzman", "Wizard of Oz", "Wicked Witch", "Prequel", "Adaption", "Film", "Visual Effects", "Pop Culture", "Fantasy", "Magic"]},
    {"title": "Gladiator II", "keywords": ["Paul Mescal", "Ridley Scott", "Pedro Pascal", "Critics", "Historical", "Roman Empire", "Rome", "Ancient", "Sequel", "Denzel Washington", "Revenge", "Power Struggle", "Visual Effects", "Cinema", "Box Office", "Connie Nielsen", "Lucius"]},
    {"title": "Moana 2", "keywords": ["Auli'i Cravalho", "Dwayne Johnson", "Critics", "Cinema", "Box Office", "Moana", "Maui", "Disney", "Animation", "Adventure", "Musical", "Fantasy", "Ocean", "Sequel", "Songs", "Soundtrack", "Polynesian"]},
    {"title": "Red One", "keywords": ["Chris Evans", "Dwayne Johnson", "Critics", "Cinema", "Box Office", "Holiday", "Film", "Lump of coal", "Amazon Studios", "Lucy Liu", "Action", "Comedy", "Santa Claus", "Entertainment", "Family", "Christmas"]},
]

def fetch_articles(movie, api_key, articles_needed_per_movie, seen_urls, outfile):
    articles_per_keyword = max(1, articles_needed_per_movie // len(movie["keywords"]))
    
    for keyword in movie["keywords"]:
        total_fetched = 0
        page = 1
        wait_time = 10  # Start with 10 seconds
        while total_fetched < articles_per_keyword:
            try:
                params = {
                    'q': f"{movie['title']} AND {keyword.lower()}",
                    'from': '2024-10-15',
                    'to': '2024-10-18',
                    'language': 'en',
                    'apiKey': api_key,
                    'pageSize': min(50, articles_per_keyword - total_fetched),
                    'page': page
                }
                url = 'https://newsapi.org/v2/everything'
                response = requests.get(url, params=params)
                
                if response.status_code == 429:
                    print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
                    time.sleep(wait_time)
                    wait_time *= 2  # Exponential backoff
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                for article in data.get('articles', []):
                    if article['url'] not in seen_urls:
                        seen_urls.add(article['url'])
                        json.dump({
                            'title': article['title'],
                            'source': article['source']['name'],
                            'publishedAt': article['publishedAt'],
                            'description': article['description'],
                            'url': article['url']
                        }, outfile)
                        outfile.write(",\n")  # Separate articles with a comma
                        total_fetched += 1
                
                page += 1
                if not data['articles']:
                    break  # No more articles for this keyword
                wait_time = 10  # Reset wait time after a successful request
                
            except requests.RequestException as e:
                print(f"An error occurred: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff after each error
        print(f"Fetched {total_fetched} unique articles with keyword '{keyword}' for '{movie['title']}'")

if __name__ == "__main__":
    seen_urls = set()
    articles_per_movie = TOTAL_ARTICLES_NEEDED // len(movies)
    
    # Open the file once and start the JSON array
    with open('movie_articles.json', 'w') as outfile:
        outfile.write("[\n")
        
        for movie in movies:
            fetch_articles(movie, API_KEY, articles_per_movie, seen_urls, outfile)
        
        # Go back to remove the last comma and close the array
        outfile.seek(outfile.tell() - 2, 0)  # Remove the last comma and newline
        outfile.write("\n]")  # Close the JSON array

    print(f"Total unique articles collected.")