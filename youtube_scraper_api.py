import requests
import json
from googleapiclient.discovery import build
import wget
import tweepy
from twitter import (consumer_key,secret_key,key,secret)
import os
import re
from youtube import api_key

youtube = build('youtube','v3',developerKey=api_key)

def get_number_of_videos():
    request = youtube.channels().list(
            id='UC-XWpctw55Q6b_AHo8rkJgw',       
            part='contentDetails').execute()



    playlist_id = request['items'][0]['contentDetails']['relatedPlaylists']['uploads']


    request2= youtube.playlistItems().list(playlistId= playlist_id,
                                            part='snippet').execute()
    
    number= request2['pageInfo']['totalResults']

    return number

total_videos = get_number_of_videos()

with open('youtubenumber.txt','r') as f:
    oldnumber = f.read()

new_videos= total_videos - int(oldnumber)

print('There are ',new_videos,' new videos')

if new_videos ==0:
    print("There are no new videos right now")
    exit()
else:
    def get_new_videos(channel_id):
        request = youtube.channels().list(
        id=channel_id,
        part='contentDetails').execute()

        playlist_id = request['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        videos=[]

        request2= youtube.playlistItems().list(playlistId= playlist_id,
                                                    part='snippet',
                                                    maxResults= new_videos).execute()

        videos += request2['items']

        return videos

    videos = get_new_videos('UC-XWpctw55Q6b_AHo8rkJgw')

    # print(len(videos))

    for video in videos:
        title= video['snippet']['title']

        video_id = video['snippet']['resourceId']['videoId']

        video_url= 'https://www.youtube.com/watch?v=' + video_id + '&ab_channel=MLGHighlights'

        auth=tweepy.OAuthHandler(consumer_key, secret_key)

        auth.set_access_token(key, secret)
        
        api=tweepy.API(auth)
        
        tweet = ("Check out this new video \n " + title + '\n' + video_url)
        
        api.update_status(tweet)

        from twilio.rest import Client

        word_list = ['career-high', 'career high', 'season-high', 'season-high']
        for video in videos:
            if any(x in title for x in word_list):
 
                account_sid = 'AC9861bca725b674a7479dcb3eb36b104e' 
                auth_token = 'a0c170ce779eaa0a21ab8d9db2dd7a87' 
                client = Client(account_sid, auth_token)
 
                message = client.messages.create( 
                              from_='+12564148992',  
                              body=title,      
                              to='+306983799114' 
                          ) 
 
apenended_number= str(total_videos)

with open('youtubenumber.txt','w') as f:
    f.write(apenended_number)













