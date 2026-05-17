import imaplib
import email
from mailparser import parse_from_bytes
import os

def fetch_latest_emails(imap_server, email_user, email_pass, limit=5):
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        mail.select("inbox")

        # Search for all emails in the inbox
        status, messages = mail.search(None, "ALL")
        if status != 'OK':
            return {"error": "Could not search inbox"}

        # Get the list of email IDs
        mail_ids = messages[0].split()
        latest_ids = mail_ids[-limit:]  # Get the last 'limit' emails
        latest_ids.reverse()  # Newest first

        emails_list = []
        for m_id in latest_ids:
            status, data = mail.fetch(m_id, "(RFC822)")
            if status != 'OK':
                continue

            raw_email = data[0][1]
            parsed_mail = parse_from_bytes(raw_email)
            
            emails_list.append({
                "subject": parsed_mail.subject,
                "from": parsed_mail.from_[0][1] if parsed_mail.from_ else "Unknown",
                "body": parsed_mail.text_plain[0] if parsed_mail.text_plain else parsed_mail.body,
                "date": str(parsed_mail.date)
            })

        mail.logout()
        return {"emails": emails_list}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage (requires real credentials)
    # print(fetch_latest_emails("imap.gmail.com", "user@gmail.com", "app_password"))
    pass
