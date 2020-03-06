from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port = 0)
            #creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)
    
    # Call the Drive v3 API
    if drive_service:
        print ('Successful connection')
            
    # Create a folder on Drive
    folderName = 'Scare Videos'
    
    #TODO: how to check if folder already exists
    #response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder', name = " + folderName)
    file_metadata = {
      'name': folderName,
      'mimeType': 'application/vnd.google-apps.folder'
    }
    root_folder = drive_service.files().create(body = file_metadata).execute()
    print('Folder \'' + folderName + '\' created')

    #upload scare cam video
    file_metadata = {'name': 'scare_02-21 22-36-22.h264'}
    media = MediaFileUpload('scare_02-21 22-36-22.h264', mimetype='video/h264')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print ('File ID: %s' % file.get('id'))

if __name__ == '__main__':
    main()