from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
import requests
import os
import uuid

app = FastAPI()

SERVICE_URL = "http://192.168.0.243:6666"
HA_URL = "http://192.168.0.222:8123"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlMmM1NTk4MWE1ODU0OGNkOTU5MDdjMzJmNWE0NGU5MyIsImlhdCI6MTc3ODc1MDkzNSwiZXhwIjoyMDk0MTEwOTM1fQ.TpTmDjIIxGNjX8QeyYl-q8yUrtK5FGfXNAKvDLPZQc0"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

SERVICES = {
    "anubhav": "notify.mobile_app_s24ultra",
    "jyoti": "notify.mobile_app_s24_plus",
}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class NotifyBody(BaseModel):
    title: str
    message: str = ""
    target: str = "anubhav"


def send_notification(service, title, message, image_url=None):
    url = f"{HA_URL}/api/services/{service.replace('.', '/')}"

    payload = {
        "title": title,
        "message": message,
    }

    if image_url:
        payload["data"] = {
            "image": image_url
        }

    return requests.post(url, headers=HEADERS, json=payload)


@app.post("/notify")
def notify(body: NotifyBody):

    targets = (
        SERVICES.values()
        if body.target == "all"
        else [SERVICES[body.target]]
    )

    results = []

    for service in targets:
        r = send_notification(service, body.title, body.message)
        results.append(r.status_code)

    return {"results": results}


@app.get("/", response_class=HTMLResponse)
def ui(request: Request):

    status = request.query_params.get("status")

    badge = ""

    if status == "success":
        badge = """
        <div class="badge success">
            Notification Sent
        </div>
        """

    elif status == "failed":
        badge = """
        <div class="badge failed">
            Failed To Send
        </div>
        """

    options = "".join(
        [f'<option value="{k}">{k}</option>' for k in SERVICES.keys()]
    )

    options += '<option value="all">ALL</option>'

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>HA Notify</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
            body {{
                font-family: Arial;
                max-width: 700px;
                margin: auto;
                padding: 20px;
                background: #111;
                color: white;
            }}

            input, textarea, select, button {{
                width: 100%;
                margin-top: 10px;
                padding: 12px;
                border-radius: 8px;
                border: none;
                box-sizing: border-box;
            }}

            textarea {{
                min-height: 180px;
                resize: vertical;
            }}

            button {{
                background: #4CAF50;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }}

            .badge {{
                padding: 12px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
                font-weight: bold;
            }}

            .success {{
                background: #1f6f3d;
            }}

            .failed {{
                background: #8b1e1e;
            }}
        </style>
    </head>

    <body>

        {badge}

        <h2>Home Assistant Notifications</h2>

        <form action="/notify-ui" method="post" enctype="multipart/form-data">

            <label>Target</label>
            <select name="target">
                {options}
            </select>

            <label>Title</label>
            <input type="text" name="title" required>

            <label>Message</label>
            <textarea name="message"></textarea>

            <label>Image (optional)</label>
            <input type="file" name="image" accept="image/*">

            <button type="submit">Send Notification</button>

        </form>

    </body>
    </html>
    """


@app.post("/notify-ui")
async def notify_ui(
    target: str = Form(...),
    title: str = Form(...),
    message: str = Form(""),
    image: UploadFile = File(None),
):

    image_url = None

    if image and image.filename:
        ext = image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"

        path = os.path.join(UPLOAD_DIR, filename)

        with open(path, "wb") as f:
            f.write(await image.read())

        image_url = f"{SERVICE_URL}/uploads/{filename}"

    targets = (
        SERVICES.values()
        if target == "all"
        else [SERVICES[target]]
    )
    
    success = True

    for service in targets:
        r = send_notification(
            service,
            title,
            message,
            image_url=image_url,
        )

        if r.status_code >= 400:
            success = False

    status = "success" if success else "failed"

    return RedirectResponse(
        url=f"/?status={status}",
        status_code=303,
    )

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
