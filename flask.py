from flask import Flask, request, jsonify
freom get_database import get_database_pages
import requests

app = Flask(__name__)

NOTION_API_TOKEN = 'YOUR_NOTION_API_TOKEN'
DATABASE_ID = 'YOUR_NOTION_DATABASE_ID'
WEBHOOK_SECRET = 'YOUR_WEBHOOK_SECRET'

@app.route('/webhook', methods=['POST'])
get_database_pages()

def retrieve_page_title(page_id):
    url = f'https://api.notion.com/v1/pages/{page_id}'
    headers = {
        'Authorization': f'Bearer {NOTION_API_TOKEN}',
        'Notion-Version': '2022-06-28',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        page_data = response.json()
        return page_data.get('properties', {}).get('title', {}).get('title', [{}])[0].get('text', {}).get('content', '')
    else:
        return None

if __name__ == '__main__':
    app.run(port=5000)
