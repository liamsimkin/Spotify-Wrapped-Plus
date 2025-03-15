import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd


load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read user-read-recently-played"
))

st.header("Top Tracks")

timePeriod = st.selectbox("", ["4 weeks", "6 months", "1 year"])
if timePeriod == "4 weeks":
    timePeriod = "short_term"
elif timePeriod == "6 months":
    timePeriod = "medium_term"
else:
    timePeriod = "long_term"

topTracks = sp.current_user_top_tracks(time_range=timePeriod, limit=50)

# Set up two columns for the main layout
cols = st.columns(2)

# Split tracks into two halves
first10 = topTracks['items'][:10]
second10 = topTracks['items'][10:20]

# Display the first half in the first column
with cols[0]:
    for i, track in enumerate(first10, start=1):
        name = track['name']
        artist = track['artists'][0]['name']
        albumCover = track['album']['images'][0]['url']  # Get the album cover image URL
        
        # Create two sub-columns for the image and text side by side
        track_cols = st.columns([1, 4])  # First column for image, second for text
        
        with track_cols[0]:  # Image column
            st.image(albumCover, width=150)  # Display the album cover

        with track_cols[1]:  # Text column
            st.markdown(f"**{i}. {name}** by *{artist}*")  # Display track details

# Display the second half in the second column
with cols[1]:
    for i, track in enumerate(second10, start=11):
        name = track['name']
        artist = track['artists'][0]['name']
        albumCover = track['album']['images'][0]['url']  # Get the album cover image URL
        
        # Create two sub-columns for the image and text side by side
        track_cols = st.columns([1, 4])  # First column for image, second for text
        
        with track_cols[0]:  # Image column
            st.image(albumCover, width=150)  # Display the album cover

        with track_cols[1]:  # Text column
            st.markdown(f"**{i}. {name}** by *{artist}*")  # Display track details




data = []
for track in topTracks['items'][20:]:
    data.append({
        "Track": track['name'],
        "Artist": track['artists'][0]['name'],
        "Album": track['album']['name'],
        "Popularity": track['popularity']
    })

df = pd.DataFrame(data)
df.index = df.index + 21
st.dataframe(df, height = 500, row_height = 50)