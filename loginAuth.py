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
    
    #Checks if a ?code is in the URL
    query_params = st.experimental_get_query_params()
    code = query_params.get("code", [None])[0]

    if code:
        #If there is a code, get the token and store it in the session
        token_info = sp_oauth.get_access_token(code)
        st.session_state['spotify_token'] = token_info["access_token"]

        # Get the user info from Spotify API
        sp = get_spotify_client()
        user_info = sp.current_user()
        st.session_state['user_id'] = user_info["id"]

        #Reload and display newly fetched user data 
        st.rerun()

    else:
        #If no code, display the login link
        auth_url = sp_oauth.get_authorize_url()
        st.markdown(f"""
            <meta http-equiv="refresh" content="0; url={auth_url}" />
            <p>Redirecting to Spotify login...</p>
            """, unsafe_allow_html=True)
        
        st.stop()

def get_spotify_client():
    if "spotify_token" in st.session_state:
            #use stored login token
        return spotipy.Spotify(auth=st.session_state['spotify_token'])
    else:
        login_spotify()