This project is a Python automation system that reads real unread emails from a Gmail inbox using the Gmail API and logs them into a Google Sheet using the Google Sheets API.
Each email is processed only once, stored without duplication, and marked as read after successful processing.
-------------------------------------------------------------------
                     High-Level Architecture Diagram
┌─────────────┐
│   Gmail     │
│ (Unread)    │
└─────┬───────┘
      │ Gmail API (OAuth 2.0)
      ▼
┌─────────────┐
│ Python App  │
│ (main.py)   │
│             │
│ - Fetch     │
│ - Parse     │
│ - Dedup     │
│ - Mark Read │
└─────┬───────┘
      │ Google Sheets API
      ▼
┌─────────────┐
│ Google Sheet│
│ Email Logs  │
└─────────────┘
-------------------------------------------------------------------
step by step installation
Step 1: Environment Setup
I installed Python 3 on my system.
ed a project folder and a virtual environment.
I installed required libraries like google-api-python-client, google-auth, and beautifulsoup4 using pip.

Step 2: Google Cloud Project Setup
I created a new project in Google Cloud Console.
Inside the project, I enabled:
Gmail API,Google Sheets API

Step 3: OAuth Configuration
I configured the OAuth Consent Screen as an External application
I added my Gmail account as a test user.
I created OAuth 2.0 Desktop credentials and downloaded the credentials.json file.
I stored this file locally and added it to .gitignore to ensure it is not committed.

Step 4: Gmail Authentication
I implemented OAuth authentication using the Gmail API.
On the first run, Google shows a consent screen.
After approval, access and refresh tokens are stored locally and reused in future runs.

Step 5: Email Fetching & Parsing
I fetched only unread emails from the inbox.
For each email, I extracted:
Sender,Subject,Date & time
Plain-text body content

Step 6: Google Sheets Setup
I created a Google Sheet manually.
I added headers: From, Subject, Date, Content.
I copied the Spreadsheet ID and configured it in the project.

Step 7: Logging Emails to Sheets
I connected to Google Sheets using OAuth.
Each processed email is appended as a new row in the sheet.

Step 8: Duplicate Prevention & State Persistence
I used Gmail message IDs as unique identifiers.
After processing an email, its ID is saved in a local JSON file.
On subsequent runs, the script checks this file and skips already processed emails.

Step 9: Marking Emails as Read
After successfully inserting an email into Google Sheets, I mark the email as read using the Gmail API.

Step 10: Re-Running the Script
If I run the script again:
No duplicate rows are added
Only new unread emails are processed
Previously processed emails are skipped
--------------------------------------------------------------------------------------------
OAuth Flow Used
This project uses OAuth 2.0 Desktop Application Flow.
User authenticates via Google Consent Screen
Access & refresh tokens are generated
Tokens are stored locally (token.pickle, token_sheets.pickle)
Tokens are reused on subsequent runs without re-login
This approach ensures secure access without storing passwords and complies with Google API security guidelines.
--------------------------------------------------------------------------------------------
Duplicate Prevention Logic
Each Gmail email has a unique message ID.
After processing an email, its message ID is stored in processed_emails.json
Before inserting into Google Sheets, the script checks if the ID already exists
If found, the email is skipped
This guarantees:
No duplicate rows
Safe re-running of the script
Idempotent behavior
--------------------------------------------------------------------------------------------
State Persistence Method
State is persisted using a local JSON file:
processed_emails.json
Why this approach:
Simple and transparent
Easy to explain and debug
Suitable for single-user automation
No external database dependency
The file stores a list of processed Gmail message IDs.
--------------------------------------------------------------------------------------------
Challenge:
Google Sheets API frequently threw range parsing errors, especially when sheet names contained spaces.

Solution:
Instead of specifying explicit column ranges, the implementation passes only the sheet name and uses:
--------------------------------------------------------------------------------------------
Limitations of the Solution
Uses local JSON file for state (not suitable for multi-user scale)
Designed for a single Gmail account
No scheduling (manual execution)
No advanced email filtering (can be added as bonus)