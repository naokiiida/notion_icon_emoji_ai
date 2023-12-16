import requests

url = 'https://api.notion.com/v1/databases/<DATABASE_ID>'
headers = {
    'Authorization': '<SECRET>',
    'Notion-Version': '2022-06-28'
}

response = requests.get(url, headers=headers)

# Check the status code to ensure the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    print(data)
else:
    print(f"Error: {response.status_code} - {response.text}")
