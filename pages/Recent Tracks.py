import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd

load_dotenv()

st.set_page_config(
    page_title="Wrapped+",
    page_icon="favicon.ico",
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

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read user-read-recently-played"
))

st.header("Recent Listening")
st.markdown("Your 50 most recently listened to tracks")

recent_tracks = sp.current_user_recently_played(limit=50)

#set up top 20 display
cols = st.columns(2)

first10 = recent_tracks['items'][:10]
second10 = recent_tracks['items'][10:20]

# display first 10 tracks
with cols[0]:
    for i, item in enumerate(first10, start=1):
        track = item['track']
        name = track['name']
        artist = track['artists'][0]['name']
        albumCover = track['album']['images'][0]['url']
        
        track_cols = st.columns([1, 4])
        
        #album art
        with track_cols[0]:
            st.image(albumCover, width=150) 

        #text
        with track_cols[1]:
            st.markdown(f"**{i}. {name}** by *{artist}*")

# display 11-20 next to it
with cols[1]:
    for i, item in enumerate(second10, start=11):
        track = item['track']
        name = track['name']
        artist = track['artists'][0]['name']
        albumCover = track['album']['images'][0]['url']
        
        track_cols = st.columns([1, 4])
        
        with track_cols[0]:
            st.image(albumCover, width=150)

        with track_cols[1]:
            st.markdown(f"**{i}. {name}** by *{artist}*")

#display 21-50 in a table below
data = []
for item in recent_tracks['items'][20:]:
    track = item['track']
    data.append({
        "Track": track['name'],
        "Artist": track['artists'][0]['name'],
        "Album": track['album']['name']
        })

df = pd.DataFrame(data)
df.index = df.index + 21 #table index
st.dataframe(df, height = 500, row_height = 50)