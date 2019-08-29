#!/usr/bin/env python
"""
basic usage of the Drive v3 API.

Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""
from __future__ import print_function

import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools


def GDriveGetService():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('token.json')

    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


# Drive v3 API
def getGDriveFileList():

    service = GDriveGetService()
    # Call the Drive v3 API
    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
    return items


def GDriveCreateFolder(name='folder', parent_id=None):

    service = GDriveGetService()

    folder_metadata = {'name': name,
                       'parents': [parent_id],
                       'mimeType': 'application/vnd.google-apps.folder'}
    create_folder = service.files().create(body=folder_metadata,
                                           fields='id').execute()
    folder_id = create_folder.get('id', [])
    return folder_id


def GDriveUploadFile(filename, description, mime_type, parent_id=None):
    service = GDriveGetService()

    file_metadata = {'name': os.path.basename(filename), 'parents': [parent_id], 'mimeType': mime_type, 'description': description}

    media = MediaFileUpload(
        os.path.join(filename),
        mimetype=mime_type)

    ufile = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return ufile




