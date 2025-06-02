import json
import pprint
import argparse
import datetime

import spotipy
from dotenv import dotenv_values
from openai import OpenAI

def main():
    config = dotenv_values(".env")
    client = OpenAI(api_key=config["APIKEY"])
    parser = argparse.ArgumentParser(description="CLI Song utility")
    parser.add_argument("-p",type=str, default="Generated Playlist - Happy songs (default)", help="Prompt to describe playlist")
    parser.add_argument("-n",type=int, default=8,help="Number of songs in playlist")
    args = parser.parse_args()
    playlist_prompt = args.p
    count = args.n
    songs = get_playlist(client,playlist_prompt, count)
    pprint.pprint(songs)
    add_songs_to_spotify(args.p,songs,config)

def get_playlist(client,prompt,count):
    example_json = """
    [
        {"song":"Happy","artist":"Pharrell Williams"},
        {"song":"Uptown Funk","artist":"Mark Ronson feat. Bruno Mars"},
        {"song":"Can't Stop the Feeling!","artist":"Justin Timberlake"},
        {"song":"Shake It Off","artist":"Taylor Swift"},
        {"song":"Roar","artist":"Katy Perry"},
        {"song":"I Gotta Feeling","artist":"The Black Eyed Peas"},
        {"song":"Good as Hell","artist":"Lizzo"},
        {"song":"Best Day of My Life","artist":"American Authors"},
        {"song":"Walking on Sunshine","artist":"Katrina and the Waves"},
        {"song":"Shut Up and Dance","artist":"WALK THE MOON"}
    ]
    """
    messages = [
        {"role":"system","content": """You are a helpful playlist generating assistant. 
        The song and artist name should match correctly (if possible as per Spotify) and it should suit the text prompt provided.
        You should return only a JSON array (no text or characters extra), where each element follows this format: {"song":<song_title},"artist":<artist_name>} """},
        {"role":"user","content":f"Generate a playlist of {count}songs based on this prompt: {prompt}"},
    #     {"role":"assistant","content":example_json},
    #     {"role":"user","content":"Generate a playlist of songs based on this prompt: High energy and dance songs"}
    ]

    response = client.chat.completions.create(
        messages = messages,
        model = "gpt-4.1-mini",
        max_tokens=300
    )
    playlist = json.loads(response.choices[0].message.content.strip())
    return playlist


def add_songs_to_spotify(playlist_prompt,songs,config):
    # Sign up as a developer and register your app at https://developer.spotify.com/dashboard/applications

    # Step 1. Create an Application.

    # Step 2. Copy your Client ID and Client Secret.
    # Use your Spotify API's keypair's Client ID
    # Use your Spotify API's keypair's Client Secret

    # Step 3. Add `http://localhost:9999` as as a "Redirect URI"
    
    # Step 4. Click `Users and Access`. Add your Spotify account to the list of users (identified by your email address)

    # Spotipy Documentation
    # https://spotipy.readthedocs.io/en/2.22.1/#getting-started


    sp = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=config["SPOCLIENT_ID"],
            client_secret=config["SPOCLIENT_SECRET"],
            redirect_uri="https://github.com/srama-krishnan",
            scope="playlist-modify-private"
        )
    )

    current_user = sp.current_user()
    assert current_user is not None

    track_ids = []
    for i in songs:
        artist, song = i["artist"],i["song"]
        query = song
        search_results = sp.search(q=query,type="track",limit = 2)
        if (
            not search_results["tracks"]["items"]
            or search_results["tracks"]["items"][0]["popularity"] < 20
        ):
            continue
        else:
            good_guess = search_results["tracks"]["items"][0]
            print(f"Found: {good_guess['name']} [{good_guess['id']}]")
            track_ids.append(good_guess["id"])
            

    created_playlist = sp.user_playlist_create(
        current_user["id"],
        public=False,
        name = f"{playlist_prompt} ({datetime.datetime.now().strftime('%c')})"
    )

    sp.user_playlist_add_tracks(current_user["id"],created_playlist["id"],track_ids)
    print("\n")
    print(f"Created playlist: {created_playlist['name']}")
    print(created_playlist["external_urls"]["spotify"])

if __name__ == "__main__":
    main()


