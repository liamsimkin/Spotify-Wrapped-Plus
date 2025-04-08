import streamlit as st
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import io
from loginAuth import get_spotify_client

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
        🎵 Wrapped+ Spotify Stats
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

#login and get details
sp = get_spotify_client()
user = sp.current_user()

#----Top Artists----
st.header("Top Artists")
st.markdown("Your top 50 artists in the specified timeframe")

timePeriod = st.selectbox("", ["1 month", "6 months", "1 year"])
if timePeriod == "1 month":
    timePeriod = "short_term"
elif timePeriod == "6 months":
    timePeriod = "medium_term"
else:
    timePeriod = "long_term"

topArtists = sp.current_user_top_artists(time_range=timePeriod, limit=50)

cols = st.columns(2)
first10 = topArtists['items'][:10]
second10 = topArtists['items'][10:20]

# display first 10 artists
with cols[0]:
    for i, artist in enumerate(first10, start=1):
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
            st.markdown(f"**{i}. {name}**")

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
            st.markdown(f"**{i}. {name}**")

#21-50 in a table
data = []
for artist in topArtists['items'][20:]:
    data.append({
        "Name": artist['name'],
        "Genres": artist['genres']
    })

df = pd.DataFrame(data)
df.index = df.index + 21 #table index
st.dataframe(df, height = 500, row_height = 50)

#----Word Cloud----
st.header("Top genres")
genres = []
for artist in topArtists['items']:
    genres.extend(artist['genres'])  # Some artists have multiple genres

genre_counts = Counter(genres)

#generate wordcloud
wc = WordCloud(width=2000, height=1000, background_color='black', colormap='viridis')
wc.generate_from_frequencies(genre_counts)

#make it an image without border
img_buffer = io.BytesIO()
wc.to_image().save(img_buffer, format='PNG')
img_buffer.seek(0)

st.image(img_buffer, use_container_width=True)