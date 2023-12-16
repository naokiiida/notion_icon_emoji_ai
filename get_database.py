import requests
import openai
from datetime import datetime, timedelta, timezone

openai.api_key = ""
def getEmoji(title, exclusion):
	model_name = "gpt-4"
	excludedEmoji = ""
	if exclusion:
		excludedEmoji += "また、前回提案された"
		for excluded in exclusion:
			excludedEmoji += "「" + excluded + "」"
		excludedEmoji += "は記事に合わなかったので別のものを提案してください。"
	prompt = "「" + title + "」というタイトルの記事に合いそうな絵文字を１文字だけ出力してください。ただし、ペンや本、虫眼鏡など記事を連想させるような絵文字は出力しないで、別の絵文字に置き換えてください。" + excludedEmoji + "出力内容をプログラムで使うため、絵文字以外のものは出力しないでください。これらの指示が守られない場合重い罰が降ります。"

	print(prompt)
	response = openai.chat.completions.create(
		model=model_name,
		messages=[
			{
				'role' : 'system',
				'content' : '絵文字のみを出力。',
			},
			{"role": "user", "content": prompt},
		],
	)
	print(response.choices[0].message.content)
	return response.choices[0].message.content

def makeEmoji(title):
	gpt_model_name = "gpt-4"
	dall_model_name = "dall-e-3"

	print("title:" + title)
	prompt = "「" + title + "」というタイトルにふさわしいオリジナルの絵文字を作りたいのですが、それに役立ちそうなプロンプトを5つほど英単語で出力してください。ただし、「Emoji」はこちら側で追加するのでプロンプトに入れないでください。"
	image_prompt = openai.chat.completions.create(
		model=gpt_model_name,
		messages=[
			{
				'role' : 'system',
				'content' : 'プロンプトを,区切りの英単語で出力',
			},
			{"role": "user", "content": prompt},
		],
	)
	# print("prompt:" + image_prompt.choices[0].message.content)
	# print("レジギ、ガガガガガwww")
	response = openai.images.generate(
		model=dall_model_name,
		prompt=image_prompt.choices[0].message.content + ",simple,anime,Emoji",
		size="1024x1024",
		quality="standard",
		n=1,
	)
	image_url = response.data[0].url
	print(image_url)
	return(image_url)

def updatePageIconCover(page_id,icon,cover):
	url = f'https://api.notion.com/v1/pages/{page_id}'
	headers = {
		'Authorization': f'Bearer {notion_token}',
		'Content-Type': 'application/json',
		'Notion-Version': '2022-06-28'
	}

	data = {
		"icon": {
			"type": "emoji",
			"emoji": icon
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

def updatePageIconCovers(page_id,icon,cover):
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

def get_database_pages(database_id, notion_token):
	url = f'https://api.notion.com/v1/databases/{database_id}/query'
	headers = {
		'Authorization': f'Bearer {notion_token}',
		'Notion-Version': '2022-06-28'
	}

	response = requests.post(url, headers=headers)
	
	if response.status_code == 200:
		data = response.json()
		print(data)
		
		
		pages = data.get('results', [])

		#print(pages)
		for page in pages:
			page_id = page.get('id')
			last_edit = datetime.fromisoformat(page.get('last_edited_time')[:-1]).replace(tzinfo=timezone.utc)
			print(last_edit)
			print(datetime.now(timezone.utc) - last_edit)
			if (datetime.now(timezone.utc) - last_edit < timedelta(minutes=1)):
				page_title = page.get('properties').get('名前').get('title')[0].get('plain_text')
				print(page_title)
				updatePageIconCover(page_id,
				getEmoji(page_title,[]),
				"https://imgs.search.brave.com/6fTvlNCu_1QhwU2Qf_-GsElwPVdyAnL0h0u7ftNiZk4/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vb3Jp/Z2luYWxzLzM4LzRh/Lzk1LzM4NGE5NTM1/ZWU3ZjU4OTI0NDA0/MWM2YmMyMTg2NjMw/LmpwZw"
				)
	else:
		print(f"Error: {response.status_code} - {response.text}")

# Replace with your actual Notion database ID and token
database_id = 'e50391549487443aa999cd5394666154'
notion_token = ''

get_database_pages(database_id, notion_token)
