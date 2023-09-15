import subprocess
from dotenv import load_dotenv
import os
from requests import get
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

def get_new_releases() -> list:
    os_path = os.getenv("OSPATH")
    with open(os_path + "artists.json", "r") as f:
        artists = json.load(f)

    releases = list()
    for key in artists.keys():
        albums = get_artists_albums(token, artists[key])
        album_list = albums['items']

        for album in album_list:
            try:
                album_date = datetime.strptime(album['release_date'], "%Y-%m-%d").date()
                if album_date == date.today():
                    releases.append([key, album['name']])
            except:
                try:
                    album_date = datetime.strptime(album['release_date'], "%Y").date()
                except:
                    print(f'--date error--\nfor:{key}\ngot:{album["release_date"]}\n--------------')
    return releases

if __name__ == "__main__":
    load_dotenv()
    token = auth.token()

    person = os.getenv("PERSON")
    phone_number = os.getenv("PHONE_NUMBER")
    os_path = os.getenv("OSPATH")
    releases = get_new_releases()
    
    message_str = generate_message(person, releases=releases)
    # print(len(message_str))
    # print(message_str)
    # os.system(f"osascript send.scpt {Phone_number} '{message_str}'")
    subprocess.run(["osascript", os_path + "send.scpt", phone_number, message_str])
