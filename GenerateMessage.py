from requests import get
import json
import auth

def generate_message(name: str, releases: list) -> str:
    msg = ""
    msg = f"{greeting(name)}\n\n{new_releases(releases)}\n\n{song_recomendation()}\n\n{joke()}"

    return msg

def greeting(name: str) -> str:
    return f"Good Morning {name}"

def new_releases(releases: list) -> str:
    if len(releases) == 0:
        return "Unfortunately no new musisc is out from artists you follow. Maybe Tomorrow!"
    music_str = "You have new music!!\n"
    
    for i in releases:
        music_str += f"{i[1]} by: {i[0]}\n"
    
    return music_str

def song_recomendation() -> str:
    # TODO
    # add paramters to the URL

    url = 'https://api.spotify.com/v1/recommendations?limit=1&market=US&seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical%2Ccountry&seed_tracks=0c6xIDDpzE81m2q797ordA'
    header = auth.header(token=auth.token())

    result = get(url, headers=header)
    json_result = json.loads(result.content)
    rec = json_result['tracks'][0]

    song_name = rec['name']
    artist_name = rec['artists'][0]['name']

    rec_str = f"Here is your recommended song for the day:\n{song_name}  by: {artist_name}"
    return rec_str

def joke() -> str:
    joke_str =  "Your daily joke:\n"
    
    result = get("https://icanhazdadjoke.com/slack")
    json_result = result.json()
    joke = json_result["attachments"][0]["text"]
    joke_str += joke
    return joke_str

song_recomendation()