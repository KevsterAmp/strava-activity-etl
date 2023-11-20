import pandas as pd
from datetime import datetime
from stravalib.client import Client
from os import environ as e
from dotenv import load_dotenv


load_dotenv()
CLIENT_ID = e.get('STRAVA_CLIENT_ID')
CLIENT_SECRET = e.get('STRAVA_CLIENT_SECRET')

client = Client()
authorize_url = client.authorization_url(
    client_id=CLIENT_ID, redirect_uri="http://localhost:8282/authorized"
)
print("Authorize in the url below \n\n")
print(authorize_url)
print("\n\n")

CODE = input("Input code here: ")

token_response = client.exchange_code_for_token(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=CODE
)
access_token = token_response["access_token"]
refresh_token = token_response["refresh_token"]
expires_at = token_response["expires_at"]

client.access_token = access_token

out = []
for activity in client.get_activities(before=datetime.now(), limit=50):
    out.append({
        "name": activity.name,
        "distance": str(activity.distance).strip("eter"),
        "elapsed_time": str(activity.moving_time),
        "link": f"https://www.strava.com/activities/{activity.id}"
    })

df = pd.DataFrame(out)
print("\n\n")
print("Last 10 Activities")
print(df.head(10))