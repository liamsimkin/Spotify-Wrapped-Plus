import spotipy
from spotipy.oauth2 import SpotifyOAuth

import streamlit as st
import pandas as pd

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="845c3692352f42508a10beebe7358c36",
    client_secret="897ea6795ac74e0cbe03e55326d789f9",
    redirect_uri="http://localhost:8888/callback",
    scope="user-top-read user-read-recently-played"
))

top_tracks = sp.current_user_top_tracks(time_range='long_term', limit=50)