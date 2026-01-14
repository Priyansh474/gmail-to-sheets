from .gmail_service import (
    get_gmail_service,
    fetch_unread_emails,
    get_email_details,
    mark_email_as_read
)
from .email_parser import parse_email
from .sheets_service import get_sheets_service, append_row
from .state_manager import load_processed_ids, save_processed_id


def main():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    processed_ids = load_processed_ids()
    emails = fetch_unread_emails(gmail_service)

    print(f"Unread emails found: {len(emails)}")

    for email in emails:
        msg_id = email["id"]

        # Prevent duplicates
        if msg_id in processed_ids:
            print(f"Skipping duplicate: {msg_id}")
            continue

        # Fetch & parse email
        message = get_email_details(gmail_service, msg_id)
        sender, subject, date, body = parse_email(message)

        # Append to Google Sheet (skip if same content already exists)
        appended = append_row(sheets_service, [sender, subject, date, body])

        # Save state so we don't reprocess this message again
        save_processed_id(msg_id)

        # Mark email as read
        mark_email_as_read(gmail_service, msg_id)

        if appended:
            print(f"Processed email: {msg_id}")
        else:
            print(f"Skipped append (duplicate content) but marked processed: {msg_id}")


if __name__ == "__main__":
    main()
