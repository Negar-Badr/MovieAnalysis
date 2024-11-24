import csv
import re
from math import log
from collections import Counter, defaultdict

stopword_file = "stopwords.txt"
csv_file = "AnnotatedArticles.csv"
output_file = "tfidf_results.txt"

def load_stopwords(stopword_file):
    """Load stopwords from a file into a set."""
    stopwords = set()
    if stopword_file:
        try:
            with open(stopword_file, 'r', encoding='utf-8') as f:
                stopwords = {line.strip().lower() for line in f}
        except Exception as e:
            print(f"Error reading stopword file {stopword_file}: {e}")
    return stopwords

def tokenize(text):
    """Tokenize text into words, removing punctuation and converting to lowercase."""
    return [word.lower() for word in re.findall(r'\b\w+\b', text) if word.lower() not in stopwords]

def compute_tf(document):
    """Compute term frequency (TF) for a single document."""
    word_counts = Counter(document)
    total_words = sum(word_counts.values())
    return {word: count / total_words for word, count in word_counts.items()}

def compute_idf(documents):
    """Compute inverse document frequency (IDF) for all terms in a set of documents."""
    num_docs = len(documents)
    doc_freq = Counter(word for doc in documents for word in set(doc))
    return {word: log(num_docs / (1 + freq)) for word, freq in doc_freq.items()}

def compute_tfidf(tf, idf):
    """Compute TF-IDF scores by combining TF and IDF."""
    return {word: tf_val * idf.get(word, 0) for word, tf_val in tf.items()}

# Load stopwords
stopwords = load_stopwords(stopword_file)

# Load CSV and organize data by categories
category_documents = defaultdict(list)

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        category = row['Categories']
        description = row['description']
        tokens = tokenize(description)
        category_documents[category].append(tokens)

# Calculate TF-IDF for each category
tfidf_scores = {}

for category, documents in category_documents.items():
    # Flatten all documents in the category into one
    merged_document = [word for doc in documents for word in doc]
    
    # Compute TF and IDF
    tf = compute_tf(merged_document)
    idf = compute_idf(documents)
    tfidf = compute_tfidf(tf, idf)
    
    # Get top 10 words with highest TF-IDF scores
    top_words = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:10]
    tfidf_scores[category] = top_words

# Write the results to a file
with open(output_file, 'w', encoding='utf-8') as f:
    for category, words in tfidf_scores.items():
        f.write(f"Category: {category}\n")
        for word, score in words:
            f.write(f"  {word}: {score:.4f}\n")
        f.write("\n")

print(f"TF-IDF results saved to {output_file}")
