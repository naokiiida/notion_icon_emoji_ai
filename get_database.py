import requests
import time
import json

notion_token = '<notion_token>'
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

def getPageIconCover(page_id, page_title):
	url = f"https://api.notion.com/v1/pages/{page_id}"

	headers = {
		"Authorization": f"Bearer {notion_token}",
		"Content-Type": "application/json",
		"Notion-Version": "2022-06-28",
	}

	response = requests.get(url, headers=headers)
	saved_data = get_saved_titles()
 
	if response.status_code == 200:
		page_data = response.json()
		# print(page_data)
		icon_type = page_data.get("icon", {}).get("type")
		print("Icon Type:", icon_type)
		if icon_type == "emoji":
			icon_emoji = page_data.get("icon", {}).get("emoji")
			print("Icon Emoji:", icon_emoji)
			saved_data[page_id] = {'title': page_title, 'icon': {"type": "emoji", "emoji": icon_emoji}}
		elif icon_type == "external":
			icon_image = page_data.get("icon", {}).get("external", {}).get("url")
			print("Icon Image:", icon_image)
			saved_data[page_id] = {'title': page_title, 'icon': {"type": "external", "external": {"url": icon_image}}}
		# Check if the title has changed
			save_saved_titles(saved_data)
	else:
		print(f"Failed to retrieve Page data. Status code: {response.status_code}")
		print(response.text)

def get_saved_titles():
	try:
		with open(titles_file, 'r') as file:
			saved_data = json.load(file)
	except FileNotFoundError:
		saved_data = {}
	return saved_data

def save_saved_titles(saved_data):
	with open(titles_file, 'w') as file:
		json.dump(saved_data, file)

def get_database_pages(database_id):
	url = f'https://api.notion.com/v1/databases/{database_id}/query'
	headers = {
		'Authorization': f'Bearer {notion_token}',
		'Notion-Version': '2022-06-28'
	}

	saved_data = get_saved_titles()

	while True:
		response = requests.post(url, headers=headers)

		if response.status_code == 200:
			data = response.json()
			pages = data.get('results', [])
			for page in pages:
				page_id = page.get('id')
				page_properties = page.get('properties', {})
				
				page_title_data = page_properties.get('Name', {}).get('title', [{}])
				if page_title_data:
					page_title = page_title_data[0].get('text', {}).get('content', '')
					print(page_title)
					if page_title != saved_data.get(page_id, {}).get('title'):
						updatePageIconCover(page_id, "https://img.icons8.com/?size=512&id=1349&format=png", "https://images.unsplash.com/photo-1699306112834-abeadd420578")
						saved_data[page_id] = {'title': page_title, 'icon': "https://img.icons8.com/?size=512&id=1349&format=png"}
				else:
					print('No changes detected.')
					getPageIconCover(page_id, page_title)
			time.sleep(5)  # Poll every 500 milliseconds
		else:
			print(f"Error: {response.status_code} - {response.text}")
# Replace with your actual Notion database ID
database_id = '<database_id>'

get_database_pages(database_id)