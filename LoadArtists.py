import json
from requests import get

import auth

def load_from_txt():
    artist_dict = {}
    with open("artists.txt", "r") as f:
        for artist in f:
            artist = artist.replace('\n','')
            artist_dict[artist] = get_artist_id(artist)
            print(f"{artist}, {artist_dict[artist]}")
    with open("artists.json", "w") as f:
        json.dump(artist_dict, f, indent=4)
    
    
def get_artist_id(artist):
    token = auth.token()
    header = auth.header(token)
    url = f"https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1&offset=0"
    result = get(url, headers=header)
    json_result = json.loads(result.content)
    return json_result['artists']['items'][0]['id']



if __name__ == "__main__":
    load_from_txt()
