from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import io
import google.auth
from googleapiclient.http import MediaIoBaseDownload
import logging

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.readonly']

def create_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_vocab_file_id(service):
    try:
        # Call the Drive v3 API
        results = service.files().list(q=f"name = 'Saved translations'").execute()
        items = results.get('files', [])
        id = items[0]["id"]
        return id
        
    except HttpError as error:
        logging.error(f'An error occurred: {error}')

def download_process():
    logging.info("Downloading vocabulary from Google Docs")
    creds = create_creds()
    service = build('drive', 'v3', credentials=creds)
    file_id = get_vocab_file_id(service)
    file_io = download_file(file_id, service)
    write_to_file(file_io)

def download_file(real_file_id, service):
    try:
        file_id = real_file_id
        request = service.files().export_media(fileId=file_id, mimeType='text/csv')
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logging.debug(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        logging.error(F'An error occurred: {error}')
        file = None

    return file

def write_to_file(file_io):
    with open("vocab.csv", 'wb') as file:
        file.write(file_io.getvalue())


if __name__ == '__main__':
    download_process()