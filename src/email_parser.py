import base64
from bs4 import BeautifulSoup

def parse_email(message):
    headers = message['payload']['headers']

    sender = subject = date = ""

    for header in headers:
        if header['name'] == 'From':
            sender = header['value']
        elif header['name'] == 'Subject':
            subject = header['value']
        elif header['name'] == 'Date':
            date = header['value']

    body = ""

    def extract_body(payload):
        if 'parts' in payload:
            for part in payload['parts']:
                extract_body(part)
        else:
            mime_type = payload.get('mimeType', '')
            if 'data' in payload.get('body', {}):
                nonlocal body
                decoded_body = base64.urlsafe_b64decode(
                    payload['body']['data']
                ).decode('utf-8', errors='ignore')
                
                # If it's HTML, parse and extract text
                if mime_type == 'text/html':
                    soup = BeautifulSoup(decoded_body, 'html.parser')
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    # Get text
                    text = soup.get_text(separator=' ', strip=True)
                    # Clean up whitespace
                    body = ' '.join(text.split())
                else:
                    # Plain text
                    body = decoded_body

    extract_body(message['payload'])

    return sender, subject, date, body
