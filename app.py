import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

url = "https://drive.google.com/uc?id=1ehsnatBnH56ZfXn8k21MQx3yibOi3O_-"
output = "similarity.pkl"

if not os.path.exists(output):
    gdown.download(url, output, quiet=False)


# fetch_poster will take movie_id then send api request to tmdb with api key inside and their response is saved
# the saved resonse is then coverted in json and saved in data, then concatenated with prior code to make the poster link complete
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        # only print index as output
        #print(i[0])
        recommended_movies.append( movies.iloc[i[0]].title)

        # fetch poster from API
        # fetch is been called and movie_id is beeen passed and response(poster link) is been appended in recommended_movies_poster list
        recommended_movies_poster.append(fetch_poster(movie_id))

        # print(movies.iloc[i[0]].title)
        # print(i[0])
    return recommended_movies, recommended_movies_poster


#loading movies data using pickle in dict datatype
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
# creating new dataframe ( movies ) and putting imported dict data in it.
# so now we have new dataframe with all data of jupyter's dataframe (new_df)
# now we will extract movies name from this and pass it in selected_movie_name
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))



st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values
)

if st.button('Recommend'):
    # calling recommend function and passing movie name(selected_movie_name)
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])