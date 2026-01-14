from src.gmail_service import get_gmail_service, fetch_unread_emails, get_email_details
from src.email_parser import parse_email
from src.sheets_service import get_sheets_service, append_row
from src.state_manager import load_processed_ids, save_processed_id


gmail_service = get_gmail_service()
sheets_service = get_sheets_service()

processed_ids = load_processed_ids()
emails = fetch_unread_emails(gmail_service)

for email in emails:
    msg_id = email['id']

    if msg_id in processed_ids:
        print(f"Skipping duplicate (already processed): {msg_id}")
        continue

    msg = get_email_details(gmail_service, email['id'])
    sender, subject, date, body = parse_email(msg)

    appended = append_row(sheets_service, [sender, subject, date, body])
    # Always save the processed id so we don't keep reprocessing
    save_processed_id(msg_id)
    if appended:
        print("Inserted into sheet")
    else:
        print("Skipped insert — duplicate content")
