import requests
import time
import json

notion_token = 'secret_vEiGYd4tasN2jXawxOMViB8DTfScCxPbVbl4RjMko1O'
titles_file = 'saved_titles.json'

def updatePageIconCover(page_id, icon, cover):
	url = f'https://api.notion.com/v1/pages/{page_id}'
	headers = {
		'Authorization': f'Bearer {notion_token}',
		'Content-Type': 'application/json',
		'Notion-Version': '2022-06-28'
	}
	data = {
		"icon": {
			"type": "external",
			"external": {
				"url": icon
			}
		},
		"cover":{
			"type": "external",
			"external": {
				"url": cover
			}
		}
	}
	response = requests.patch(url, headers=headers, json=data)
	# Check the response status code
	if response.status_code == 200:
		print("Page updated successfully.")
	else:
		print(f"Error: {response.status_code} - {response.text}")

def get_saved_titles():
	try:
		with open(titles_file, 'r') as file:
			saved_titles = json.load(file)
	except FileNotFoundError:
		saved_titles = {}
	return saved_titles

def save_titles(saved_titles):
	with open(titles_file, 'w') as file:
		json.dump(saved_titles, file)

def get_database_pages(database_id):
	url = f'https://api.notion.com/v1/databases/{database_id}/query'
	headers = {
		'Authorization': f'Bearer {notion_token}',
		'Notion-Version': '2022-06-28'
	}

	saved_titles = get_saved_titles()

	while True:
		response = requests.post(url, headers=headers)

		if response.status_code == 200:
			data = response.json()
			pages = data.get('results', [])

			for page in pages:
				page_id = page.get('id')
				page_exist = page.get('properties', {}).get('Name', {}).get('title', [{}])
				if page_exist != []:
					page_title = page_exist[0].get('text', {}).get('content', '')
					# Check if the title has changed
					if page_title != saved_titles.get(page_id):
						updatePageIconCover(page_id,
						"https://imgs.search.brave.com/DtVTOsx_ECkKFm32s50AyGA3CrNVg5twdUuKUuZzBPg/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTAw/ODk4MTkxNC92ZWN0/b3Ivc21pbGV5LXll/bGxvdy1pY29uLXZl/Y3Rvci1lbW90aWNv/bi1oYXBweS1mYWNl/LmpwZz9zPTYxMng2/MTImdz0wJms9MjAm/Yz0zU0ZsOWEydFEy/RW5rV2dyZUJES3Va/a3VvWlZRdEpfRmFM/YngtYTdTNV8wPQ",
						"https://imgs.search.brave.com/6fTvlNCu_1QhwU2Qf_-GsElwPVdyAnL0h0u7ftNiZk4/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vb3Jp/Z2luYWxzLzM4LzRh/Lzk1LzM4NGE5NTM1/ZWU3ZjU4OTI0NDA0/MWM2YmMyMTg2NjMw/LmpwZw"
						)
						saved_titles[page_id] = page_title
					else:
						print('No changes detected.')
			time.sleep(5)  # Poll every 500 milliseconds
		else:
			print(f"Error: {response.status_code} - {response.text}")
# Replace with your actual Notion database ID
database_id = '2287890a69204371a0d1ad892885f5ef'

get_database_pages(database_id)