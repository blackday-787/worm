from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Docs read-only scope
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def main():
    # Authenticate and create the service
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('docs', 'v1', credentials=creds)

    # Your specific Google Doc ID
    DOCUMENT_ID = '1QkkuHI3JivqNJWHG2Za6NYviGrDkjv_l02AiQktW46E'
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()

    # Extract and print text content
    for element in doc['body']['content']:
        if 'paragraph' in element:
            for text_run in element['paragraph'].get('elements', []):
                text = text_run.get('textRun', {}).get('content')
                if text:
                    print(text, end='')

if __name__ == '__main__':
    main()
