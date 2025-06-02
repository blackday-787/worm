from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

app = Flask(__name__)
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

@app.route('/get-doc-content', methods=['POST'])
def get_doc_content():
    doc_id = request.json.get('doc_id')
    if not doc_id:
        return jsonify({'error': 'Missing doc_id'}), 400

    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('docs', 'v1', credentials=creds)

    doc = service.documents().get(documentId=doc_id).execute()

    content = ""
    for element in doc['body']['content']:
        if 'paragraph' in element:
            for text_run in element['paragraph'].get('elements', []):
                text = text_run.get('textRun', {}).get('content')
                if text:
                    content += text
    return jsonify({'content': content})

if __name__ == '__main__':
    app.run(port=5000)
