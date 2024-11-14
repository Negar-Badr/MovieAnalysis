import requests
import json
import time

API_KEY = '863a63a8004a4063a52b0f6f4a86c9aa'
TOTAL_ARTICLES_NEEDED = 100
movies = [
    {"title": "Wicked", "keywords": ["Ariana Grande ", "Jon M. Chu", "Cynthia Erivo", "Critics", "Cinema", "Box Office", "Glinda", "Elphaba", "Musical", "Stephen Schwartz", "Winnie Holzman", "Wizard of Oz", "Wicked Witch", "Prequel", "Adaption", "Film", "Visual Effects", "Pop Culture", "Fantasy", "Magic"]},
    {"title": "Gladiator II", "keywords": ["Paul Mescal", "Ridley Scott", "Pedro Pascal", "Critics", "Historical", "Roman Empire", "Rome", "Ancient", "Sequel", "Denzel Washington", "Revenge", "Power Struggle", "Visual Effects", "Cinema", "Box Office", "Connie Nielsen", "Lucius"]},
    {"title": "Moana 2", "keywords": ["Auli'i Cravalho", "Dwayne Johnson", "Critics", "Cinema", "Box Office", "Moana", "Maui", "Disney", "Animation", "Adventure", "Musical", "Fantasy", "Ocean", "Sequel", "Songs", "Soundtrack", "Polynesian"]},
    {"title": "Red One", "keywords": ["Chris Evans", "Dwayne Johnson", "Critics", "Cinema", "Box Office", "Holiday", "Film", "Lump of coal", "Amazon Studios", "Lucy Liu", "Action", "Comedy", "Santa Claus", "Entertainment", "Family", "Christmas"]},
]

def fetch_articles(movie, api_key, articles_needed_per_movie, seen_urls):
    articles = []
    articles_per_keyword = articles_needed_per_movie // len(movie["keywords"])
    
    for keyword in movie["keywords"]:
        total_fetched = 0
        page = 1
        while total_fetched < articles_per_keyword:
            params = {
                'q': f"{movie['title']} AND {keyword.lower()}",
                'from': '2024-10-20',
                'to': '2024-11-14',
                'language': 'en',
                'apiKey': api_key,
                'pageSize': min(100, articles_per_keyword - total_fetched),
                'page': page
            }
            url = 'https://newsapi.org/v2/everything'
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                for article in data['articles']:
                    # Check for duplicates using the URL
                    if article['url'] not in seen_urls:
                        seen_urls.add(article['url'])
                        articles.append({
                            'title': article['title'],
                            'source': article['source']['name'],
                            'publishedAt': article['publishedAt'],
                            'description': article['description'],
                            'url': article['url']  # Include URL for reference
                        })
                        total_fetched += 1
                page += 1
                if not data['articles']:  # No more articles found
                    break
            time.sleep(1)  # Delay to avoid hitting rate limit
        print(f"Fetched {total_fetched} unique articles with keyword '{keyword}' for '{movie['title']}'")
    return articles

if __name__ == "__main__":
    all_articles = []
    seen_urls = set()  # Set to track unique URLs
    articles_per_movie = TOTAL_ARTICLES_NEEDED // len(movies)
    for movie in movies:
        movie_articles = fetch_articles(movie, API_KEY, articles_per_movie, seen_urls)
        all_articles.extend(movie_articles)

    with open('movie_articles.json', 'w') as outfile:
        json.dump(all_articles, outfile)
    print(f"Total unique articles collected: {len(all_articles)}")
