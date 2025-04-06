import os
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth
import spotipy

def login_spotify():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-library-read user-top-read user-read-recently-played playlist-modify-public playlist-modify-private",
        cache_handler = spotipy.cache_handler.MemoryCacheHandler()
    )

    if "spotify_token" in st.session_state:
        return spotipy.Spotify(auth=st.session_state.spotify_token)
    
    query_params = st.experimental_get_query_params()
    code = query_params.get("code", [None])[0]

    if code:
        # If we have a code, we get the token and store it in the session
        token_info = sp_oauth.get_access_token(code)
        st.session_state['spotify_token'] = token_info["access_token"]

        # Get the user info from Spotify API
        sp = get_spotify_client()  # Assuming get_spotify_client uses the token
        user_info = sp.current_user()
        st.session_state['user_id'] = user_info["id"]

        # Proceed with re-run to reload the session state and fetch user data
        st.rerun()

    else:
        # If we don't have a code yet, display the login link
        auth_url = sp_oauth.get_authorize_url()
        st.title("🎵 Wrapped+")
        st.markdown("To continue, please log in with Spotify:")
        st.markdown(f"[👉 Login with Spotify]({auth_url})", unsafe_allow_html=True)
        st.stop()

def get_spotify_client():
    if "spotify_token" in st.session_state:
        # Return Spotify client using the stored token
        return spotipy.Spotify(auth=st.session_state['spotify_token'])
    else:
        # If no token, force the login process
        login_spotify()