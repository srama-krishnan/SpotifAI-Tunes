
import json
import pprint
import argparse
import datetime
import os
import logging

import spotipy
from dotenv import dotenv_values
from openai import OpenAI  # ✅ new SDK

def main():
    config = dotenv_values(".env")

    client = OpenAI(api_key=config["APIKEY"])  # ✅ required fix

    parser = argparse.ArgumentParser(description="CLI Song utility")
    parser.add_argument(
        "-p", type=str, default="Generated Playlist - Happy songs (default)", help="Prompt to describe playlist"
    )
    parser.add_argument(
        "-n", type=int, default=8, help="Number of songs in playlist"
    )
    args = parser.parse_args()

    playlist_prompt = args.p
    count = args.n

    songs = get_playlist(client, playlist_prompt, count)
    pprint.pprint(songs)

    add_songs_to_spotify(playlist_prompt, songs, config)


def get_playlist(client, prompt, count):
    messages = [
        {"role": "system", "content": """You are a helpful playlist generating assistant. 
Only respond with a JSON array of objects in the format: 
{"song": <song_title>, "artist": <artist_name>}.
Match artist and song names correctly."""},
        {"role": "user", "content": f"Generate a playlist of {count} songs for: {prompt}"}
    ]

    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",  # ✅ updated
        max_tokens=300
    )

    content = response.choices[0].message.content.strip()
    return json.loads(content)


def add_songs_to_spotify(playlist_prompt, songs, config):
    sp = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=config["SPOCLIENT_ID"],
            client_secret=config["SPOCLIENT_SECRET"],
            redirect_uri="http://localhost:9999",  # ✅ should be same as set in Spotify Dashboard
            scope="playlist-modify-private"
        )
    )

    current_user = sp.current_user()
    assert current_user is not None

    track_ids = []
    for track in songs:
        song, artist = track["song"], track["artist"]
        query = f"track:{song} artist:{artist}"
        search_results = sp.search(q=query, type="track", limit=1)

        if not search_results["tracks"]["items"]:
            continue

        best_match = search_results["tracks"]["items"][0]
        print(f"Found: {best_match['name']} by {best_match['artists'][0]['name']}")
        track_ids.append(best_match["id"])

    if not track_ids:
        print("No valid tracks found.")
        return

    playlist = sp.user_playlist_create(
        current_user["id"],
        public=False,
        name=f"{playlist_prompt} ({datetime.datetime.now().strftime('%c')})"
    )

    sp.user_playlist_add_tracks(current_user["id"], playlist["id"], track_ids)

    print("\n🎵 Created playlist:")
    print(playlist["external_urls"]["spotify"])


if __name__ == "__main__":
    main()
