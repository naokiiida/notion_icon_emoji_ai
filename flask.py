from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NOTION_API_TOKEN = 'YOUR_NOTION_API_TOKEN'
DATABASE_ID = 'YOUR_NOTION_DATABASE_ID'
WEBHOOK_SECRET = 'YOUR_WEBHOOK_SECRET'

@app.route('/webhook', methods=['POST'])
def notion_webhook():
    data = request.get_json()

    # Verify the webhook secret for added security
    if data.get('secret') != WEBHOOK_SECRET:
        return 'Invalid Secret', 403

    # Check if the event is a new page creation
    if data.get('parent') and data['parent']['type'] == 'database_id' and data['parent']['database_id'] == DATABASE_ID:
        page_id = data.get('id')
        page_title = retrieve_page_title(page_id)

        # Process the page title as needed (e.g., print or save to a database)
        print(f"New Page Title: {page_title}")

    return jsonify({'success': True})

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
