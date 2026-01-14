import os
import pickle
import base64

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Gmail scope: read + modify (mark as read)
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def get_gmail_service():
    """
    Authenticates the user and returns a Gmail API service object
    """
    creds = None

    # token.pickle stores the user's access & refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials available, login required
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def fetch_unread_emails(service):
    """
    Fetch unread emails from inbox
    """
    messages = []
    page_token = None

    while True:
        params = {
            'userId': 'me',
            'labelIds': ['INBOX', 'UNREAD'],
            'maxResults': 500
        }
        if page_token:
            params['pageToken'] = page_token

        results = service.users().messages().list(**params).execute()
        if not results:
            break

        messages.extend(results.get('messages', []))

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return messages

def get_email_details(service, message_id):
    """
    Fetch full email data using message ID
    """
    message = service.users().messages().get(
        userId='me',
        id=message_id,
        format='full'
    ).execute()
    return message

def mark_email_as_read(service, message_id):
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={
            'removeLabelIds': ['UNREAD']
        }
    ).execute()


