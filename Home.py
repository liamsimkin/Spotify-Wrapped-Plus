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
        🎵 Wrapped+ | Your Spotify Insights
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

st.header("Top Tracks")
st.markdown("Your top 50 tracks in the specified timeframe")

timePeriod = st.selectbox("", ["1 month", "6 months", "1 year"])
if timePeriod == "1 month":
    timePeriod = "short_term"
elif timePeriod == "6 months":
    timePeriod = "medium_term"
else:
    timePeriod = "long_term"

topTracks = sp.current_user_top_tracks(time_range=timePeriod, limit=50)

#set up top 20 display
cols = st.columns(2)

first10 = topTracks['items'][:10]
second10 = topTracks['items'][10:20]

# display first 10 tracks
with cols[0]:
    for i, track in enumerate(first10, start=1):
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
    for i, track in enumerate(second10, start=11):
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
for track in topTracks['items'][20:]:
    data.append({
        "Track": track['name'],
        "Artist": track['artists'][0]['name'],
        "Album": track['album']['name']
    })

df = pd.DataFrame(data)
df.index = df.index + 21 #table index
st.dataframe(df, height = 500, row_height = 50)