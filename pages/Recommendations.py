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
st.markdown("Recommended artists - based on your listening")

button_placeholder = st.empty()

top_artists = sp.current_user_top_artists(time_range="long_term", limit=50)

genres = []
for artist in top_artists['items']:
    genres.extend(artist['genres'])  # Some artists have multiple genres

genre_counts = Counter(genres)
genre_list = list(genre_counts.keys())[:5]
recommended_artists = []
recommended_tracks = []

for i in genre_list:
# Example: Search for artists in the 'pop' genre
    results = sp.search(q='genre:' + i, type='artist', limit=5)
    # Print the artists found
    for artist in results['artists']['items']:
        recommended_artists.append(artist)
        top_track_list = sp.artist_top_tracks(artist['id'])
        top_track = [(track["name"], track["uri"]) for track in top_track_list["tracks"][:1]]
        recommended_tracks.append(top_track)

cols = st.columns(2)

first10 = recommended_artists[:10]
second10 = recommended_artists[10:20]

# display first 10 artists
with cols[0]:
    for i, artist in enumerate(first10, start=1):
        name = artist['name']
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
            st.markdown(f"""**{name}**  
            *{genres if genres else 'n/a'}*  
            <a href="https://open.spotify.com/track/{recommended_tracks[i-1][0][1].split(':')[-1]}" target="_blank" style="text-decoration: none; color: #1DB954;">
            🎧 {recommended_tracks[i-1][0][0]}
            </a>
            """, unsafe_allow_html=True)      
            
            
            #if genres == "":
            #    st.markdown(f"*n/a*")
            #else:
            #    st.markdown(f"*{genres}*")
            #st.markdown(f"[🎵 {track[i][0]}]({track[i][1].replace('spotify:track:', 'https://open.spotify.com/track/')})")

# display 11-20 next to it
with cols[1]:
    for i, artist in enumerate(second10, start=11):
        name = artist['name']
        artistPicture = artist['images'][0]['url']
        genres = artist['genres']
        if genres != []:
            genres = genres[0]
        else:
            genres = ""
        
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
            st.markdown(f"""**{name}**  
            *{genres if genres else 'n/a'}*  
            <a href="https://open.spotify.com/track/{recommended_tracks[i-1][0][1].split(':')[-1]}" target="_blank" style="text-decoration: none; color: #1DB954;">
            🎧 {recommended_tracks[i-1][0][0]}
            </a>
            """, unsafe_allow_html=True) 

def createRecommendedPlaylist():
    print("b")
    user_id = sp.current_user()["id"]

    playlist_name = "Recommended Tracks"
    playlist_desc = "My recommended tracks from Wrapped+"

    playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_desc)
    #for track in recommended_tracks:
    #    sp.playlist_add_items(playlist["id"], track[0][1].split(':')[-1])

    track_uris = [track[0][1].split(':')[-1] for track in recommended_tracks]  # Extract the full URIs
    sp.playlist_add_items(playlist["id"], track_uris)

if button_placeholder.button("🎵 Create Playlist"):
    createRecommendedPlaylist()