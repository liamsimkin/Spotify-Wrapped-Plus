import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import io

load_dotenv()

st.set_page_config(
    page_title="Wrapped+",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <div style='
        background-color: #1DB954;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 2rem;
    '>
        🎵 Wrapped+ Your Spotify Insights
    </div>
    <style>
        .main {
            background-color: #000000 !important;
            color: white !important;
        }

        /* Set the sidebar background to dark grey */
        section[data-testid="stSidebar"] {
            background-color: #121212 !important;
        }

        /* Make all content background black */
        html, body, [class*="css"] {
            background-color: #000000 !important;
            color: white !important;
        }

        /* Optional: Hide Streamlit footer */
        footer {visibility: hidden;}

        /* Optional: Customize the table headers to be white */
        .e1b2p2ww10, .e1b2p2ww11 {
            color: white !important;
        }
        /* sidebar width */
        section[data-testid="stSidebar"] {
            width: 200px !important;
        }
        
        /* sidebar option width */
        section[data-testid="stSidebar"] > div:first-child {
            width: 250px !important;
        }
    </style>
""", unsafe_allow_html=True)

#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
#    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
#    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
#    scope="user-top-read user-read-recently-played user-library-read"
#))

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read user-library-read playlist-modify-public playlist-modify-private"
)

sp = spotipy.Spotify(auth_manager=sp_oauth)

#----Top Artists----
st.header("Recommendations")
st.markdown("Your recommendations")

top_artists = sp.current_user_top_artists(time_range="medium_term", limit=20)


topArtists = sp.current_user_top_artists(time_range="long_term", limit=50)

genres = []
for artist in topArtists['items']:
    genres.extend(artist['genres'])  # Some artists have multiple genres

genre_counts = Counter(genres)
genre_list = list(genre_counts.keys())[:5]
#print(list(genre_counts.keys())[:5])
recommended_artists = []

for i in genre_list:
# Example: Search for artists in the 'pop' genre
    results = sp.search(q='genre:' + i, type='artist', limit=5)
    # Print the artists found
    for artist in results['artists']['items']:
        recommended_artists.append(artist)
        #print(f"Artist: {artist['name']} - {artist['external_urls']['spotify']}")

#print(recommended_artists['artists']['items'][1])
print(recommended_artists[1]['name'])

cols = st.columns(2)

first10 = recommended_artists[:10]
second10 = recommended_artists[10:20]

# display first 10 artists
with cols[0]:
    for i, artist in enumerate(first10, start=1):
        name = artist['name']
        #url = artist['spotify']
        genres = artist['genres']
        if genres != []:
            genres = genres[0]
        else:
            genres = ""
        artistPicture = artist['images'][0]['url']
        
        artistCols = st.columns([1, 4])
        
        #album art
        with artistCols[0]:
            st.markdown(f"""
                <div style='
                    width: 100px;
                    height: 100px;
                    overflow: hidden;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background-color: #1e1e1e;
                '>
                    <img src="{artistPicture}" style="height: 100%; object-fit: cover;">
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        #text
        with artistCols[1]:
            st.markdown(f"**{name}**")
            if genres == "":
                st.markdown(f"*n/a*")
            else:
                st.markdown(f"*{genres}*")

# display 11-20 next to it
with cols[1]:
    for i, artist in enumerate(second10, start=11):
        name = artist['name']
        artistPicture = artist['images'][0]['url']
        
        artistCols = st.columns([1, 4])
        #album art
        with artistCols[0]:
            st.markdown(f"""
                <div style='
                    width: 100px;
                    height: 100px;
                    overflow: hidden;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background-color: #1e1e1e;
                '>
                    <img src="{artistPicture}" style="height: 100%; object-fit: cover;">
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        #text
        with artistCols[1]:
            st.markdown(f"{name}")