import logging
from crawler      import crawl_all_queries, save_leads_to_csv
from email_sender import run_email_campaign
from config       import OUTPUT_CSV

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("hackveda.log"),
        logging.StreamHandler()
    ]
)

def main():
    print("=" * 50)
    print("  HACKVEDA — Digital Marketing Pipeline")
    print("=" * 50)

    print("\n[Phase 1] Crawling Google for leads...")
    leads = crawl_all_queries()
    save_leads_to_csv(leads)
    print(f"✅ {len(leads)} leads saved to {OUTPUT_CSV}")

    proceed = input("\n[Phase 2] Send outreach emails? (yes/no): ").strip().lower()

    if proceed == "yes":
        stats = run_email_campaign(
            leads         = leads,
            subject       = "Free Digital Growth Audit — Hackveda",
            sender_name   = "Hackveda Team",
            delay_seconds = 6,
        )
        print(f"\n📧 Campaign Complete!")
        print(f"   Sent:    {stats['sent']}")
        print(f"   Failed:  {stats['failed']}")
        print(f"   Skipped: {stats['skipped']}")
    else:
        print("Email campaign skipped.")

if __name__ == "__main__":
    main()