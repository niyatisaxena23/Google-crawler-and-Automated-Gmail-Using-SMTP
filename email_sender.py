import smtplib
import logging
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from config import GMAIL_ADDRESS, GMAIL_APP_PASS, SMTP_HOST, SMTP_PORT
from email_templates import get_outreach_template

log = logging.getLogger(__name__)


def send_email(to_address, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASS)
            server.sendmail(GMAIL_ADDRESS, [to_address], msg.as_string())

        log.info(f"✅ Email sent to {to_address}")
        return True

    except smtplib.SMTPAuthenticationError:
        log.error("❌ Authentication failed. Check GMAIL_APP_PASS in .env")
    except Exception as e:
        log.error(f"❌ Error: {e}")

    return False


def run_email_campaign(leads, subject, sender_name, delay_seconds=5):
    stats = {"sent": 0, "failed": 0, "skipped": 0}

    for lead in leads:
        raw_emails = lead.get("emails", "N/A")

        if raw_emails == "N/A" or not raw_emails.strip():
            stats["skipped"] += 1
            continue

        email_list = [e.strip() for e in raw_emails.split(",") if e.strip()]
        company    = lead.get("title", "your company")

        for email in email_list:
            html_body = get_outreach_template(
                recipient_name = "Team",
                company        = company,
                sender_name    = sender_name,
            )
            success = send_email(email, subject, html_body)
            stats["sent" if success else "failed"] += 1
            time.sleep(delay_seconds)

    return stats


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")

    test_to = input("Enter your own email to test: ").strip()
    html = get_outreach_template("Test User", "Test Company", "Hackveda Team")
    result = send_email(test_to, "Test Email from Hackveda", html)
    print("✅ Email sent!" if result else "❌ Failed — check logs.")