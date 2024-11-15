import json

def check_uniqueness(input_file, output_file=None):
    try:
        # Load articles from the JSON file
        with open(input_file, 'r') as infile:
            articles = json.load(infile)

        print(f"Total articles loaded: {len(articles)}")

        # Use a set to track unique URLs
        unique_urls = set()
        unique_articles = []

        for article in articles:
            url = article.get('url')  # Get the URL of the article
            if url not in unique_urls:
                unique_urls.add(url)
                unique_articles.append(article)

        print(f"Unique articles found: {len(unique_articles)}")

        # Save the deduplicated articles to a new file if specified
        if output_file:
            with open(output_file, 'w') as outfile:
                json.dump(unique_articles, outfile, indent=4)
            print(f"Deduplicated articles saved to: {output_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except json.JSONDecodeError:
        print(f"Error: File '{input_file}' is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "movie_articles.json"  # Replace with your JSON file name
    output_file = "unique_movie_articles.json"  # Replace or set to None if you don't want to save the output
    check_uniqueness(input_file, output_file)
