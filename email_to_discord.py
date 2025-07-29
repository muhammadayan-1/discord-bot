import imaplib
import email
import time
import requests

# ---- CONFIGURATION ----
GMAIL_USER = "your_email@gmail.com"
GMAIL_APP_PASSWORD = "your_app_password"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/xxxxxxxx"

# ---- FUNCTION TO CHECK EMAIL ----
def check_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    mail.select("inbox")

    result, data = mail.search(None, "UNSEEN")
    ids = data[0].split()
    
    for email_id in ids:
        result, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["subject"]
        from_email = msg["from"]
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        # Send to Discord
        data = {
            "content": f"📩 **New Signal Received!**\n**Subject:** {subject}\n\n{body}"
        }
        requests.post(DISCORD_WEBHOOK_URL, json=data)
        print("✅ Signal sent to Discord")

    mail.logout()

# ---- LOOP CHECKING ----
while True:
    try:
        check_email()
    except Exception as e:
        print("❌ Error:", e)
    time.sleep(15)
