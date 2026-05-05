from fastapi import FastAPI
import requests
import re

app = FastAPI()

VIDEO_PAGE = "https://jockantv.eu/video/ujt0e"

def get_video_link():
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(VIDEO_PAGE, headers=headers, timeout=10)
    html = r.text

    match = re.search(r'https://[^"]+Download\?api_key=[^"]+', html)

    if match:
        return match.group(0)

    return None


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/video")
def video():
    link = get_video_link()

    if not link:
        return {"status": "error", "message": "no video found"}

    return {"status": "ok", "url": link}
