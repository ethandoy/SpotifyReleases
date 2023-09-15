import base64
import json
from requests import post
from dotenv import load_dotenv
import os


def token() -> str:
    """
    Generate a token based on Cliend ID and Client Secret
    given in .env file
    :return: token as a string
    """
    load_dotenv()
    # get cliend id and secret and properly encode it
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    encoded_auth = (client_id + ":" + client_secret).encode("utf-8")
    b64_auth = str(base64.b64encode(encoded_auth), "utf-8")
    
    # send api call with encoded secret and id
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + b64_auth,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    result = post(url, headers=headers, data=data)

    # parse result to return token
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

def header(token):
    """
    Generate a header for the API call
    :param str token: authentication token
    :return: API header 
    """
    return {"Authorization": "Bearer " + token}