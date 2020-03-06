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
            creds = flow.run_local_server(port = 0)
            #creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    #build the instance for api calls
    drive_service = build('drive', 'v3', credentials=creds)
    if drive_service:
        print ('Successful connection')

    # Create a folder for scare videos on drive account
    folderName = 'Scare Videos'


    results = drive_service.files().list(
        q="mimeType=\'application/vnd.google-apps.folder\' and name = \'" + folderName + "\' and trashed = false",
        pageSize = 1,
        fields = 'files(id, name)').execute()
    if not results.get('files', []): 
        file_metadata = {
        'name': folderName,
        'mimeType': 'application/vnd.google-apps.folder'
        }
        root_folder = drive_service.files().create(body = file_metadata).execute()
        print('Folder \'%s\' created' % folderName)

    #upload scare cam video
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