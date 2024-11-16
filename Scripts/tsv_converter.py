import json
import csv

def json_to_csv(json_file, tsv_file):
    # Load the JSON data from a file
    with open(json_file, 'r') as json_file:
        data = json.load(json_file)
    with open(tsv_file, 'w', newline='', encoding='utf-8') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t')  # Set delimiter to tab
        
        # Write the header
        header = ['title', 'source', 'publishedAt', 'description', 'url']
        writer.writerow(header)
        
        # Write the data rows
        for entry in data:
            row = [entry.get('title', ''), entry.get('source', ''), entry.get('publishedAt', ''), entry.get('description', ''), entry.get('url', '')]
            writer.writerow(row)



if __name__ == '__main__':
    json_to_csv('random_sample_200_articles.json', 'random_sample_200_articles.tsv')