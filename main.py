import os, requests,base64
from flask import Flask,render_template
from dotenv import load_dotenv
load_dotenv("environ.env")
client_id=os.getenv('SPOTIFY_CLIENTID')
client_secret=os.getenv('SPOTIFY_SECRET')
songs=[]

def get_access_token(client_id, client_secret):
  url="https://accounts.spotify.com/api/token"
  headers={'Content-Type':'application/x-www-form-urlencoded'}
  data={'grant_type':'client_credentials'}
  auth=(client_id, client_secret)
  response=requests.post(url,headers=headers, data=data, auth=auth)
  token_data=response.json()
  access_token=token_data.get('access_token')
  return access_token

playlist_id="37i9dQZEVXbMDoHDwVN2tF"
access_token=get_access_token(client_id, client_secret)
url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
headers={'Authorization':f'Bearer {access_token}'}
response=requests.get(url, headers=headers)
playlist_data=response.json()
for track in playlist_data['items']:
  track_id=track['track']['id']
  track_url=f"https://api.spotify.com/v1/tracks/{track_id}"
  cover_url=track['track']['album']['images'][0]['url']
  cover_response=requests.get(cover_url)
  cover_content=cover_response.content
  cover_base64=base64.b64encode(cover_content).decode('utf-8')
  song_info=f"{track['track']['name']}-{track['track']['artists'][0]['name']}-{cover_base64}\n"
  
  songs.append(song_info)




app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", songs=songs)

if __name__ == "__main__":
    app.run(debug=True)
