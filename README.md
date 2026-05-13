# Tampa Bay Restaurant Recommender

A machine learning-based restaurant recommendation system built with Python and Streamlit.  
The web application helps users discover restaurants in the Tampa Bay area based on either:
- a restaurant name (find similar places)
- a cuisine or search query (e.g., "Italian food", "BBQ", "tacos")

---

## Live Demo
https://tampa-bay-restaurant-recommender.streamlit.app

---

## Features
- Search by restaurant name or cuisine
- Filter by Tampa Bay cities using a dropdown
- Displays restaurant name, address, city, and rating
- Clickable restaurant links that open Google Maps directions

---

## How It Works
- Yelp dataset filtered to restaurants in the Tampa Bay area
- Each restaurant is represented as a text profile using categories and attributes
- TF-IDF vectorization is applied to convert text into numerical vectors
- Cosine similarity is computed to measure either:
  * restaurant-to-restaurant similarity
  * query-to-restaurant similarity
- The system returns the highest scoring restaurants as recommendations

---

## Tech Stack
- Python
- Streamlit (frontend UI)
- Pandas (data processing)
- Scikit-learn (TF-IDF + cosine similarity)
- RapidFuzz (fuzzy matching)
- NumPy

---

## Setup & Installation
### 1. Clone repo
```bash
https://github.com/AdamGeorgee/Tampa-Bay-Restaurant-Recommender.git
cd Tampa-Bay-Restaurant-Recommender
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Run app
```bash
streamlit run app.py
```
