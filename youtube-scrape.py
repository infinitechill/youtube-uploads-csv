#! /usr/local/bin/python3

'''
python script to create a csv file of 
all the current videos on your youtube channel


adapted from google / youtube api doc examples

'''

import argparse,os,re,csv
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def single_quotes(s1):
    return "'{}'".format(s1)

# Authorize the request and store authorization credentials.
def get_authenticated_service():
	flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
	credentials = flow.run_console()
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_my_uploads_list():
	channels_response = youtube.channels().list(
	mine=True,
	part='contentDetails'
	).execute()
	for channel in channels_response['items']:
		return channel['contentDetails']['relatedPlaylists']['uploads']
	return None

def list_my_uploaded_videos(uploads_playlist_id):
	playlistitems_list_request = youtube.playlistItems().list(
	playlistId=uploads_playlist_id,
	part='snippet',
	maxResults=5
	)
	mylist=[]
	while playlistitems_list_request:
		playlistitems_list_response = playlistitems_list_request.execute()
		for playlist_item in playlistitems_list_response['items']:
			video=[]
			title = str(playlist_item['snippet']['title'])
			video_id = str(playlist_item['snippet']['resourceId']['videoId'])
			url="https://www.youtube.com/watch?v="+video_id
			video.append(title)
			video.append(url)
			mylist.append(video)
		playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)
	return mylist

if __name__ == '__main__':
	youtube = get_authenticated_service()
	try:
		uploads_playlist_id = get_my_uploads_list()
		if uploads_playlist_id:
			mylist=list_my_uploaded_videos(uploads_playlist_id)
		else:
			print('There is no uploaded videos playlist for this user.')
	except Exception as e:
		print ('An HTTP error occurred:\n%s' % (e))

	myfile = open("output.csv", 'w')
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for row in mylist:
		wr.writerow( row )

