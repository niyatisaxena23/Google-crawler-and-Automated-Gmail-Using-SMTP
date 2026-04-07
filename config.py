import os
from dotenv import load_dotenv

load_dotenv()

# Search queries for your niche — edit these!
SEARCH_QUERIES = [
    "digital marketing agency India",
    "SEO company Bangalore",
    "social media marketing startup",
]

MAX_RESULTS_PER_QUERY = 10
CRAWL_DELAY_SECONDS   = 2
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

GMAIL_ADDRESS  = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASS = os.getenv("GMAIL_APP_PASS")
SMTP_HOST      = "smtp.gmail.com"
SMTP_PORT      = 587

OUTPUT_CSV = "leads.csv"