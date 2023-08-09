from dotenv import load_dotenv
import os
from requests import post, get
import json
from datetime import date, datetime
import auth
from GenerateMessage import generate_message



def get_artists_albums(token, id) -> str:
    url = f"https://api.spotify.com/v1/artists/{id}/albums?include_groups=album%2Csingle&limit=50"
    header = auth.header(token=token)

    result = get(url, headers=header)
    json_result = json.loads(result.content)
    return json_result

if __name__ == "__main__":
    token = auth.token()

    current_user = 'Nina'
    
    with open("artists.json", "r") as f:
        artists = json.load(f)

    releases = list()
    for key in artists.keys():
        albums = get_artists_albums(token, artists[key])
        album_list = albums['items']

        for album in album_list:
            try:
                album_date = datetime.strptime(album['release_date'], "%Y-%m-%d").date()
                if album_date == date.today():
                    # print(f"New Release from {key}! Album: {album['name']}")
                    releases.append([key, album['name']])
            except:
                try:
                    album_date = datetime.strptime(album['release_date'], "%Y").date()
                except:
                    print(f'--date error--\nfor:{key}\ngot:{album["release_date"]}\n--------------')


    # print(f"______sending message to {people[0][1]}______\n\n")
    message_str = generate_message("Nina", releases=releases)
    os.system(f"osascript send.scpt 7037171722 '{message_str}'")

