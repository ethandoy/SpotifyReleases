import subprocess
from dotenv import load_dotenv
import os
from requests import get
import json
from datetime import date, datetime
import auth
from GenerateMessage import generate_message


def get_artists_albums(token, id) -> str:
    """
    Spotify API call to get an artists albums
    :param str token: Authentication token required for API call
    :param str id: Unique ID of spotify artist
    :return: Json string
    """
    url = f"https://api.spotify.com/v1/artists/{id}/albums?include_groups=album%2Csingle&limit=50"
    header = auth.header(token=token)
    result = get(url, headers=header)
    
    #convert to json
    json_result = json.loads(result.content)
    return json_result

def get_new_releases() -> list:
    """
    Checks all the albums of each artist in artists.json
    to check for new releases
    :return: list of strings represnting new releases
    """
    os_path = os.getenv("OSPATH")
    with open(os_path + "artists.json", "r") as f:
        artists = json.load(f)

    releases = list()
    for key in artists.keys():
        # get list of all albums for each artist
        albums = get_artists_albums(token, artists[key])
        album_list = albums['items']

        for album in album_list:
            # check release date of each album
            try:
                album_date = datetime.strptime(album['release_date'], "%Y-%m-%d").date()
                if album_date == date.today():
                    # if it was released today we want to add it to releases
                    releases.append([key, album['name']])
            except:
                try:
                    album_date = datetime.strptime(album['release_date'], "%Y").date()
                except:
                    print(f'--date error--\nfor:{key}\ngot:{album["release_date"]}\n--------------')
    return releases

if __name__ == "__main__":
    load_dotenv()
    # call auth.py for spotify API authentication
    token = auth.token()

    # get important environment variables
    person = os.getenv("PERSON")
    phone_number = os.getenv("PHONE_NUMBER")
    os_path = os.getenv("OSPATH")

    releases = get_new_releases()
    message_str = generate_message(person, releases=releases)
    # send text message
    subprocess.run(["osascript", os_path + "send.scpt", phone_number, message_str])
