import time
from playwright.sync_api import sync_playwright


def run_browser(url, chat_id, bot):
    try:
        with sync_playwright() as p:
            bot.send_message(chat_id, "Launching Chromium...")

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                ],
            )
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1920, "height": 1080},
            )
            page = context.new_page()

            bot.send_message(chat_id, "Navigating to page...")
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            time.sleep(3)

            bot.send_message(chat_id, "Looking for buttons...")
            buttons = ["Start", "Continue", "Claim", "Next", "Visit"]

            for btn in buttons:
                try:
                    el = page.get_by_text(btn, exact=False).first
                    if el.is_visible():
                        bot.send_message(chat_id, f"Clicking '{btn}'...")
                        el.click()
                        time.sleep(4)
                except Exception:
                    pass

            bot.send_message(chat_id, "Waiting 30 seconds...")
            time.sleep(30)
            bot.send_message(chat_id, "Finished. Check Earnaldo.")
            browser.close()

    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}")
