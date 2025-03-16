import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd

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

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read user-read-recently-played"
))

st.header("Top Artists")
st.markdown("Your top 50 tracks in the specified timeframe")

timePeriod = st.selectbox("", ["4 weeks", "6 months", "1 year"])
if timePeriod == "4 weeks":
    timePeriod = "short_term"
elif timePeriod == "6 months":
    timePeriod = "medium_term"
else:
    timePeriod = "long_term"

topArtists = sp.current_user_top_artists(time_range=timePeriod, limit=50)

cols = st.columns(2)

first10 = topArtists['items'][:10]
second10 = topArtists['items'][10:20]

# display first 10 tracks
with cols[0]:
    for i, artist in enumerate(first10, start=1):
        name = artist['name']
        artistPicture = artist['images'][0]['url']
        
        artistCols = st.columns([1, 4])
        
        #album art
        with artistCols[0]:
            #st.image(artistPicture, width=150)
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
            #st.image(artistPicture, width=150)
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        #text
        with artistCols[1]:
            st.markdown(f"{i}. {name}")

# display 11-20 next to it
with cols[1]:
    for i, artist in enumerate(second10, start=11):
        name = artist['name']
        artistPicture = artist['images'][0]['url']
        
        artistCols = st.columns([1, 4])
        
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
            #st.image(artistPicture, width=150)
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)


        with artistCols[1]:
            st.markdown(f"{i}. {name}")


data = []
for artist in topArtists['items'][20:]:
    data.append({
        "Name": artist['name'],
        "Popularity": artist['popularity']
    })

df = pd.DataFrame(data)
df.index = df.index + 21 #table index
st.dataframe(df, height = 500, row_height = 50)
