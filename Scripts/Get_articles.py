import requests
import json
import time

API_KEY = ''
TOTAL_ARTICLES_NEEDED = 300
MAX_PAGES = 5  # Limit the number of pages per keyword
movies = [
    {"title": "Wicked", "keywords": ["Ariana Grande", "Jon M. Chu", "Cynthia Erivo", "Critics", "Cinema", "Box Office"]},
    {"title": "Gladiator II", "keywords": ["Paul Mescal", "Ridley Scott", "Pedro Pascal", "Critics", "Denzel Washington", "Cinema", "Box Office", "Connie Nielsen"]},
    {"title": "Moana 2", "keywords": ["Auli'i Cravalho", "Dwayne Johnson", "Critics", "Cinema", "Box Office", "Disney"]},
    {"title": "Red One", "keywords": ["Chris Evans", "Dwayne Johnson", "Critics", "Cinema", "Box Office", "Amazon Studios", "Lucy Liu"]},
]

def fetch_articles(movie, api_key, articles_needed_per_movie):
    articles = []
    articles_per_keyword = articles_needed_per_movie // len(movie["keywords"])
    
    for keyword in movie["keywords"]:
        total_fetched = 0
        page = 1
        while total_fetched < articles_per_keyword and page <= MAX_PAGES:
            params = {
                'q': f"{movie['title']} AND {keyword.lower()}",
                'from': '2024-11-8',
                'to': '2024-11-14',
                'language': 'en',
                'apiKey': api_key,
                'pageSize': min(300, articles_per_keyword - total_fetched),
                'page': page
            }
            url = 'https://newsapi.org/v2/everything'
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if not data['articles']:  # No more articles found
                        break
                    for article in data['articles']:
                        articles.append({
                            'title': article['title'],
                            'source': article['source']['name'],
                            'publishedAt': article['publishedAt'],
                            'description': article['description'],
                            'url': article['url']
                        })
                        total_fetched += 1
                    page += 1
                else:
                    print(f"Error: Received status code {response.status_code} for '{movie['title']}' with keyword '{keyword}'")
                    break
            except Exception as e:
                print(f"Exception occurred for '{movie['title']}' with keyword '{keyword}': {e}")
                break
            time.sleep(0.5)  # Delay to avoid hitting rate limit
        print(f"Fetched {total_fetched} articles with keyword '{keyword}' for '{movie['title']}'")
    return articles

if __name__ == "__main__":
    
    all_articles = []
    articles_per_movie = TOTAL_ARTICLES_NEEDED // len(movies)
    for movie in movies:
        print(f"Fetching articles for '{movie['title']}'...")
        movie_articles = fetch_articles(movie, API_KEY, articles_per_movie)
        all_articles.extend(movie_articles)

    with open('movie_articles.json', 'w') as outfile:
        json.dump(all_articles, outfile)
    print(f"Total articles collected: {len(all_articles)}")
