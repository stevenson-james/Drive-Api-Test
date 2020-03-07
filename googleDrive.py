'''
    Author: James Stevenson
    Section: 2
    File: googleDrive.py
    
    Description:
    This is a test file to be implemented in the scare cam
    IoT device. It authenticates a user onto a google drive
    account, and adds a folder and video to the account if
    they have not already been added
'''

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']

def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # If you want to reset account, delete pickle file
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Sign-in for drive account
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the instance for api calls
    drive_service = build('drive', 'v3', credentials=creds)
    if drive_service:
        print ('Successful connection')

    # Create a folder for scare videos on drive account
    folderName = 'Scare Videos'
    # Get any current instance of folder in drive account
    results = drive_service.files().list(
        q="mimeType=\'application/vnd.google-apps.folder\' and name = \'" + folderName + "\' and trashed = false",
        pageSize = 1,
        fields = 'files(id, name)').execute()
    # If folder doesn't already exist, add to account
    if not results.get('files', []):
        file_metadata = {
        'name': folderName,
        'mimeType': 'application/vnd.google-apps.folder'
        }
        root_folder = drive_service.files().create(body = file_metadata).execute()
        print('Folder \'%s\' created' % folderName)

    # Upload scare cam video (using same process as adding a folder above)
    # fileName should be changed based on current video
    fileName = 'scare_02-21 22-36-22.h264'
    results = drive_service.files().list(
        q="mimeType=\'video/h264\' and name = \'" + fileName + "\' and trashed = false",
        pageSize = 1,
        fields = 'files(id, name)').execute()
    if not results.get('files', []):
        file_metadata = {'name': fileName}
        media = MediaFileUpload(fileName, mimetype='video/h264')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
        print ('File \'%s\' added' % file.get('name'))

if __name__ == '__main__':
    main()