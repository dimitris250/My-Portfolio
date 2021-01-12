# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:54:45 2021

@author: Dim
"""

import requests
from spotify import (client_id, client_secret)
import base64
import json

url= 'https://accounts.spotify.com/api/token'

authheaders= {}

authdata={}
# curl -X "POST" -H "Authorization: Basic ZjM4ZjAw...WY0MzE=" -d grant_type=client_credentials https://accounts.spotify.com/api/token

def get_access_token(client_id,client_secret):
    message = f"{client_id}:{client_secret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    
    # print(base64_message)
    
    authheaders['Authorization']="Basic " + base64_message
    authdata['grant_type']= "client_credentials"
    
    resp=requests.post(url, headers=authheaders, data=authdata)
    
    respobject= resp.json() 
    
# print(json.dumps(respobject, indent=2))

    access_token= respobject['access_token']
    
    return access_token


# curl -H "Authorization: Bearer NgCXRKc...MzYjw" https://api.spotify.com/v1/tracks/2TpxZ7JUBn3uw46aR7qd6V

def get_playlist_tracks(access_token, playlist_id):
    
    playlist = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    
    Playlistheader= {"Authorization": "Bearer " + access_token}
    
    resp1 = requests.get(playlist, headers=Playlistheader)
    
    playlistresp = resp1.json()
    
    return playlistresp
    
    
access_token = get_access_token(client_id,client_secret)


playlist_id= input('Please enter the Playlist-Id: ')

spotify_playlist= get_playlist_tracks(access_token,playlist_id)

#print(json.dumps(lists))

with open('playlist.json','w') as f:
    json.dump(spotify_playlist, f)


playlist_sum=0

for duration in spotify_playlist['tracks']['items']:
    time_lenght = duration['track']['duration_ms']
    playlist_sum += time_lenght




for track in spotify_playlist['tracks']['items']:
    for artist in track['track']['artists']:
        print('----------------------')
        print(artist['name'],'-' ,track['track']['name'])

print('************************ \n')
print('The duration of the Playlists is :',round((playlist_sum)/60000,2), ' minutes')
print('\n ************************')

    
    





