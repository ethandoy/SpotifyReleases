from requests import get
import json
import auth

def generate_message(name: str, releases: list) -> str:
    msg = ""
    msg = f"{greeting(name)}\n{new_releases(releases)}\n{song_recomendation()}\n{joke()}"

    return msg

def greeting(name: str) -> str:
    return f"Good Morning {name}"

def new_releases(releases: list) -> str:
    if len(releases) == 0:
        return "No new musisc is out from your artists. Maybe Tomorrow!"
    music_str = "New Music!\n"
    
    for i in releases:
        music_str += f"{i[1]} by: {i[0]}\n"
    
    return music_str

def song_recomendation() -> str:
    # TODO
    # add paramters to the URL
    base_url = 'https://api.spotify.com/v1/recommendations?'
    limit_url = 'limit=1'
    market_url = '&market=US'
    artist_url = '&seed_artists=3r5D13Q9I4sLrC1bsJK0gR'
    genre_url = '&seed_genres=indie'
    track_url = '&seed_tracks=72BwjgUuMQuUzvuPmrEvEf'
    acousticness = '&target_acousticness=.5'
    danceability = '&target_danceability=.5'
    energy = '&target_energy=.5'
    instrumentalness = '&target_instrumentalness=.5'
    loudness = '&target_loudness=.5'
    popularity = '&target_popularity=.5'
    speechiness = '&target_speechiness=.5'

   


    url = base_url+limit_url+market_url+artist_url+genre_url+track_url
    #+acousticness+danceability+energy+instrumentalness+loudness+popularity+speechiness
    header = auth.header(token=auth.token())

    result = get(url, headers=header)
    json_result = json.loads(result.content)

    rec = json_result['tracks'][0]

    song_name = rec['name']
    artist_name = rec['artists'][0]['name']

    rec_str = f"Have you listened to:\n{song_name} by: {artist_name}"
    return rec_str

def joke() -> str:
    joke_str =  "Today's joke:\n"
    
    result = get("https://icanhazdadjoke.com/slack")
    json_result = result.json()
    joke = json_result["attachments"][0]["text"]
    joke_str += joke
    return joke_str