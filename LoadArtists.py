import json
from requests import get
from collections import OrderedDict
import webbrowser
import time

import auth

def load_from_txt(validate):
    artist_dict = {}
    with open("artists.txt", "r") as f:
        for artist in f:
            artist = artist.replace('\n','').lower().title()
            artist_dict[artist] = get_artist_id(artist)
            print(f"{artist}, {artist_dict[artist]}")
            if validate: validate_result(artist_dict[artist])

    artist_dict = OrderedDict(sorted(artist_dict.items()))

    with open("artists.json", "w") as f:
        json.dump(artist_dict, f, indent=4)
    
    
def get_artist_id(artist):
    token = auth.token()
    header = auth.header(token)
    url = f"https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1&offset=0&market=US"

    result = get(url, headers=header)
    json_result = json.loads(result.content)
    return json_result['artists']['items'][0]['id']

def validate_result(id):
    webbrowser.open_new_tab(f"https://open.spotify.com/artist/{id}")
    input()
    

if __name__ == "__main__":
    load_from_txt(validate=True)

