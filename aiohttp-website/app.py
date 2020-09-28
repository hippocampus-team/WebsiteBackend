import httplib2
import pprint
import sys
from apiclient.discovery import build

# The API key of the project.
API_KEY = 'AIzaSyBh_Z3FtFxRb-Mht02QTT9YS5eDS4wJE-0'


def createDriveService():
    """Builds and returns a Drive service object authorized with the
    application's service account.

    Returns:
        Drive service object.
    """

    return build('drive', 'v2')


service = createDriveService()


def recurse(parent):
    def recurseFolders():
        result = []
        page_token = None
        while True:
            param = {"q": "'" + parent + "' in parents and mimeType =  'application/vnd.google-apps.folder'"}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()
            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break

        for folder in result:
            recurse(folder.get("id"))

    def printChildren():
        result = []
        page_token = None
        while True:
            param = {"q": "'" + parent + "' in parents and mimeType != 'application/vnd.google-apps.folder'"}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()
            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break

        for afile in result:
            # Cannot use webViewLink, because it's only valid for static html content
            print(afile.get('title') + u':' + u'"' + afile.get("webContentLink") + u',"')

    recurseFolders()
    printChildren()


recurse('1dZqghGgr91yyXqU6vwDsTnAAg8S7otwV')
