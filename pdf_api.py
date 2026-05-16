import time
import requests

def upload_pdf(session: requests.Session, file_path: str, upload_url: str) -> str:
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f, 'application/pdf')}
        resp = session.post(upload_url, files=files)
    resp.raise_for_status()
    task_id = resp.json().get("taskId")
    if not task_id:
        raise Exception("No taskId in response")
    return task_id

def wait_for_processing(session: requests.Session, task_id: str, status_url: str, timeout=120):
    start = time.time()
    while time.time() - start < timeout:
        resp = session.get(f"{status_url}/{task_id}")
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "complete":
                return True
            elif data.get("status") == "failed":
                return False
        time.sleep(2)
    return False

def download_processed_pdf(session: requests.Session, task_id: str, download_url: str) -> bytes:
    resp = session.get(f"{download_url}/{task_id}")
    resp.raise_for_status()
    return resp.content