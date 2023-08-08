import base64
import json
from requests import post
from dotenv import load_dotenv
import os


def token() -> str:
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    encoded_auth = (client_id + ":" + client_secret).encode("utf-8")
    b64_auth = str(base64.b64encode(encoded_auth), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + b64_auth,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

def header(token):
    return {"Authorization": "Bearer " + token}