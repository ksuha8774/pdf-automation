import requests

def send_to_another_site(session: requests.Session, file_content: bytes, target_url: str) -> dict:
    files = {'file': ('processed_result.pdf', file_content, 'application/pdf')}
    resp = session.post(target_url, files=files)
    resp.raise_for_status()
    return resp.json()