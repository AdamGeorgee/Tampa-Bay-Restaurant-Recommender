import pandas as pd
import helper
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, utils

num_recommendations = 5

df = pd.read_csv("dataset.csv")
df = df.reset_index(drop = True)
# Use indices to find rows by name
indices = pd.Series(df.index, index = df["name"]).drop_duplicates()

# Ignore less important words
custom_stop_words = [
    "restaurant",
    "restaurants",
    "food",
    "foods",
    "cuisine",
    "cuisines",
    "place",
    "places",
    "eat",
    "eats",
    "eating",
    "meal",
    "dining"
]
all_stop_words = list(ENGLISH_STOP_WORDS.union(custom_stop_words))

# Create vectorizer without stop words and using a 2-word range
vectorizer = TfidfVectorizer(stop_words=all_stop_words, ngram_range=(1,2))
# Compute the TF-IDF matrix using the tags column
tfidf_matrix = vectorizer.fit_transform(df["tags"])

# Compute cosine similiarity matrix of every restaurant with each other
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

def restaurant_search(name, city):
    if not name:
        # If only a city is entered, return the top rated restaurants in that city
        if city:
            filtered_df = df[df["city"] == city]
            return filtered_df.sort_values(by=["stars", "review_count"], ascending=False).head(num_recommendations)[["name", "address", "city", "stars", "review_count"]]
        # If nothing is entered, return nothing
        else:
            return df.iloc[0:0]

    # If exact name not found, extract the best match
    if name not in indices:
        match = process.extractOne(name, indices.index, processor=utils.default_process)
        
        # If the match is close, use it
        if match and match[1] > 90:
            print("RESTAURANT")
            name = match[0]
        else:
            print("QUERY")
            return query_search(name, city)
    
    # Get restaurant index
    index = indices[name]
    if isinstance(index, pd.Series):
        index = index.iloc[0]

    # Create list with an index and similarity score for all restaurants
    scores = list(enumerate(similarity_matrix[index]))
    # Sort the restaurants by similarity from highest to lowest
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Get name of inputted restaurant
    input_name = df["name"].iloc[index]
    restaurant_indices = []
    seen_names = set()

    for i, score in sorted_scores:
        # Only include relevant restaurants
        if score < 0.1:
            break
        
        # Get candidate restaurant name
        candidate_name = df["name"].iloc[i]

        # Don't recommend the same name
        if candidate_name == input_name:
            continue
        if candidate_name in seen_names:
            continue
        
        # Only include restaurants in the city selected
        if city:
            if df["city"].iloc[i] != city:
                continue

        seen_names.add(candidate_name)
        restaurant_indices.append(i)

        # Limit number of recommendations
        if len(restaurant_indices) >= num_recommendations:
            break

    if len(restaurant_indices) > 0:
        return df[["name", "address", "city", "stars", "review_count"]].iloc[restaurant_indices]
    else:
        return df.iloc[0:0]

def query_search(query, city):
    query = helper.normalize_text(query)

    # Convert query into a TF-IDF vector
    query_vec = vectorizer.transform([query])
    # Compute cosine similarity for query and all restaurants
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    # Create list with an index and similarity score for all restaurants
    scores  = list(enumerate(scores))
    # Sort the restaurants by similarity from highest to lowest
    sorted_scores  = sorted(scores, key=lambda x: x[1], reverse=True)

    restaurant_indices = []
    seen_names = set()

    for i, score in sorted_scores :
        # Only include relevant restaurants
        if score < 0.1:
            break

        # Get candidate restaurant name
        candidate_name = df["name"].iloc[i]

        # Don't recommend the same name
        if candidate_name in seen_names:
            continue

        # Only include restaurants in the city selected
        if city:
            if df["city"].iloc[i] != city:
                continue

        seen_names.add(candidate_name)
        restaurant_indices.append(i)

        # Limit number of recommendations
        if len(restaurant_indices) >= num_recommendations:
            break

    if len(restaurant_indices) > 0:
        return df[["name", "address", "city", "stars", "review_count"]].iloc[restaurant_indices]
    else:
        return df.iloc[0:0]