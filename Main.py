from dotenv import load_dotenv
import os
from requests import post, get
import json
import datetime
import auth



def get_artists_albums(token, id) -> str:
    url = f"https://api.spotify.com/v1/artists/{id}/albums?limit=50"
    header = auth.header(token=token)

    result = get(url, headers=header)
    json_result = json.loads(result.content)
    return json_result

if __name__ == "__main__":
    token = auth.token()
    AJR_ID = "6s22t5Y3prQHyaHWUN1R1C"
    albums = get_artists_albums(token, AJR_ID)

    with open('res.json', 'w') as f:
        json.dump(albums, f, indent=4)

    album_list = albums['items']
    for idx, alb in enumerate(album_list):
        print(f"{idx+1}. { alb['name']} , {alb['release_date']}")