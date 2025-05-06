import streamlit as st
from collections import Counter
from loginAuth import get_spotify_client

st.set_page_config(
    page_title="Track Stats",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <div style='
        background-color: #1DB954;
        padding: 1rem;
        border-radius: 4px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 2rem;
    '>
        🎵 Track Stats - Your Music Stats
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

#login, and get details
sp = get_spotify_client()
user = sp.current_user()

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

#Get recommendations from their top artists
for i in genre_list:
    results = sp.search(q='genre:' + i, type='artist', limit=5)

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
        url = artist['external_urls']['spotify']

        artistCols = st.columns([1, 4])
        
        #album art
        with artistCols[0]:
            st.markdown(f"""
                <a href="{url}" target="_blank" style="text-decoration: none;">
                    <div style='
                        width: 100px;
                        height: 100px;
                        overflow: hidden;
                        border-radius: 4px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        background-color: #1e1e1e;
                    '>
                        <img src="{artistPicture}" style="height: 100%; object-fit: cover;">
                    </div>
                </a>
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
        
        url = artist['external_urls']['spotify']
        artistCols = st.columns([1, 4])
        #album art
        with artistCols[0]:
            st.markdown(f"""
                <a href="{url}" target="_blank" style="text-decoration: none;">
                    <div style='
                        width: 100px;
                        height: 100px;
                        overflow: hidden;
                        border-radius: 4px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        background-color: #1e1e1e;
                    '>
                        <img src="{artistPicture}" style="height: 100%; object-fit: cover;">
                    </div>
                </a>
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

#Create a playlist with the recommended tracks
def createRecommendedPlaylist():
    print("b")
    user_id = sp.current_user()["id"]

    playlist_name = "Recommended Tracks"
    playlist_desc = "My recommended tracks from Wrapped+"

    playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_desc)

    track_uris = [track[0][1].split(':')[-1] for track in recommended_tracks]  # Extract the full URIs
    sp.playlist_add_items(playlist["id"], track_uris)

if button_placeholder.button("🎵 Create playlist on your account"):
    createRecommendedPlaylist()
    st.toast("🎵 Playlist created!", icon="🎶")

st.markdown("Content provided by Spotify")