import streamlit as st
import pickle
import requests

# Function to fetch movie posters from TMDb
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f4f099e2e914f305e997656f16f4e715&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies with their names and posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

st.header("Movie Recommender System") # adds title of the interface

movies = pickle.load(open('movie_list.pkl','rb')) #loads the pickle file dumped in jupyter notebook
similarity = pickle.load(open('similarity.pkl','rb'))


movie_list = movies['title'].values # extracts the titles of the movies
selected_movie = st.selectbox( # creates a dropdown menu
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])