import streamlit as st
from helper import tampa_bay_cities
from main import restaurant_search
import urllib.parse

def make_link(name, address, city):
    query = f"{name} {address} {city}"
    encoded_query = urllib.parse.quote(query)
    return f"https://www.google.com/maps/search/?api=1&query={encoded_query}"

st.markdown(
    "<h1 style='white-space: nowrap; text-align: center;'>Tampa Bay Restaurant Recommender</h1>", 
    unsafe_allow_html=True
)
st.write("")
st.write("")

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    query = st.text_input("", placeholder="Search restaurant or cuisine", label_visibility="collapsed")

with col2:
    cities = ["Any City"] + sorted(tampa_bay_cities)
    city = st.selectbox("", cities, label_visibility="collapsed")

with col3:
    search_clicked = st.button("Search")

st.divider()

if search_clicked:
    if city == "Any City":
        selected_city = None
    else:
        selected_city = city

    results = restaurant_search(query, selected_city)

    if results.empty:
        st.warning("No restaurants found")
    else:
        for _, row in results.iterrows():
            maps_url = make_link(row["name"], row["address"], row["city"])
            st.markdown(
                f"""
                <a href="{maps_url}" target="_blank" style="text-decoration: none; color: inherit;">
                    <h3 style="margin-bottom: 0;">{row['name']}</h3>
                </a>
                """,
                unsafe_allow_html=True
            )
            st.write(f"{row['address']}, {row['city']}")
            st.write(f"⭐ {row['stars']} / 5.0 ({row['review_count']})")
            st.divider()