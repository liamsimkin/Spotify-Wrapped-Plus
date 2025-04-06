import os
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth
import spotipy

def login_spotify():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-private user-top-read user-read-recently-played playlist-modify-public playlist-modify-private"
    )

    # Check if redirected with a code
    query_params = st.experimental_get_query_params()
    code = query_params.get("code", [None])[0]

    if code and "spotify_token" not in st.session_state:
        token_info = sp_oauth.get_access_token(code)
        st.session_state.spotify_token = token_info["access_token"]
        st.rerun()

    # Not logged in yet
    if "spotify_token" not in st.session_state:
        auth_url = sp_oauth.get_authorize_url()
        st.title("🎵 Wrapped+")
        st.markdown("To continue, please log in with Spotify:")
        st.markdown(f"[👉 Login with Spotify]({auth_url})", unsafe_allow_html=True)
        st.stop()

def get_spotify_client():
    if "spotify_token" in st.session_state:
        return spotipy.Spotify(auth=st.session_state.spotify_token)
    else:
        login_spotify()
