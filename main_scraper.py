import os
import json
from playwright.sync_api import sync_playwright

# Configs
LOGIN_URL = "https://www.pexels.com/login/"
USERNAME = "dummy_name"
PASSWORD = "password"
SESSION_FILE = "session.json"

def save_session(context):
    context.storage_state(path=SESSION_FILE)

def load_session(playwright):
    if os.path.exists(SESSION_FILE):
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state=SESSION_FILE)
        return browser, context
    return None, None

def login_and_save_session(p):
    browser = p.chromium.launch(headless=False, slow_mo=100)
    context = browser.new_context()
    page = context.new_page()

    # Go to Pexels login
    page.goto(LOGIN_URL)

    # Fill email and password (using name attributes)
    page.fill("input[name='email']", USERNAME)
    page.fill("input[name='password']", PASSWORD)

    # Click login button by text
    page.get_by_role("button", name="Log in").click()

    # Wait for redirect to homepage
    page.wait_for_url("https://www.pexels.com/", timeout=15000)

    # Save session
    context.storage_state(path=SESSION_FILE)
    print("✅ Session saved to session.json")

    return browser, context

def main():
    with sync_playwright() as p:
        browser, context = load_session(p)
        if not context:
            print("No session found. Logging in...")
            browser, context = login_and_save_session(p)

        page = context.new_page()
        page.goto("https://www.pexels.com/")
        print("Successfully landed on homepage")

        browser.close()

if __name__ == "__main__":
    main()
