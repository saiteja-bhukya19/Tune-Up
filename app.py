import pickle
import pandas as pd
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + poster_path



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    "What would you like to watch today?",
    movies['title'].values
)


if st.button('Show Recommendation'):
    recommended_movie,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie[4])
        st.image(recommended_movie_posters[4])
