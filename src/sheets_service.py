import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Import config from project root
from config import SPREADSHEET_ID, SHEET_NAME

# Google Sheets scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_sheets_service():
    """
    Authenticates and returns Google Sheets API service
    """
    creds = None
    token_path = 'token_sheets.pickle'

    # Load existing token
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(
                    os.path.dirname(__file__),
                    '..',
                    'credentials',
                    'credentials.json'
                ),
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


def append_row(service, row_data):
    """
    Appends a single row to the Google Sheet
    """
    body = {
        'values': [row_data]
    }

    # Ensure sheet exists
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheet_id = None
    for sheet in spreadsheet['sheets']:
        if sheet['properties']['title'] == SHEET_NAME:
            sheet_id = sheet['properties']['sheetId']
            break

    if sheet_id is None:
        raise ValueError(f"Sheet '{SHEET_NAME}' not found in spreadsheet")

    # Check for duplicate row content before appending
    range_name = f"'{SHEET_NAME}'!A:Z"
    existing = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute().get('values', [])

    def normalize(cell):
        return ' '.join(cell.split()).strip() if isinstance(cell, str) else str(cell)

    # Compare only the number of columns provided in row_data
    cols = len(row_data)
    for r in existing:
        # pad row to cols
        row_slice = r[:cols] if len(r) >= cols else r + [''] * (cols - len(r))
        if all(normalize(a) == normalize(b) for a, b in zip(row_slice, row_data)):
            # Duplicate found; skip append
            return False

    # Append since not found
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    return True


def row_exists(service, row_data):
    """Return True if a matching row exists in the sheet."""
    range_name = f"'{SHEET_NAME}'!A:Z"
    existing = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute().get('values', [])

    def normalize(cell):
        return ' '.join(cell.split()).strip() if isinstance(cell, str) else str(cell)

    cols = len(row_data)
    for r in existing:
        row_slice = r[:cols] if len(r) >= cols else r + [''] * (cols - len(r))
        if all(normalize(a) == normalize(b) for a, b in zip(row_slice, row_data)):
            return True
    return False
