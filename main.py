from fastapi import FastAPI
from playwright.sync_api import sync_playwright
import re

app = FastAPI()

VIDEO_PAGE = "https://jockantv.eu/video/ujt0e"


def extract_video_link():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        page = browser.new_page()

        video_link = None

        def handle_response(response):
            nonlocal video_link
            if "Download?api_key=" in response.url:
                video_link = response.url

        page.on("response", handle_response)

        page.goto(VIDEO_PAGE, wait_until="networkidle", timeout=60000)

        page.wait_for_timeout(5000)

        browser.close()

        return video_link


@app.get("/")
def home():
    return {"status": "running", "engine": "playwright"}


@app.get("/video")
def video():
    try:
        link = extract_video_link()

        if not link:
            return {"status": "error", "message": "video link not found"}

        return {"status": "ok", "url": link}

    except Exception as e:
        return {"status": "error", "message": str(e)}
