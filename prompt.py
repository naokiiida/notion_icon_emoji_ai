# -*- coding: utf-8 -*-

import openai

def getEmoji(title):


	openai.api_key = ""
	model_name = "gpt-4"
	prompt = "「" + title + "」というタイトルの記事に合いそうな絵文字を１文字だけ出力してください。ただし、ペンや本、虫眼鏡など記事を連想させるような絵文字は出力しないで、別の絵文字に置き換えてください。出力内容をプログラムで使うため、絵文字以外のものは出力しないでください。これらの指示が守られない場合重い罰が降ります。"

	#print(prompt)
	response = openai.ChatCompletion.create(
		model=model_name,
		messages=[
			{
				'role' : 'system',
				'content' : '絵文字のみを出力。',
			},
			{"role": "user", "content": prompt},
		],
	)
	#print(response.choices[0]["message"]["content"])
	return response.choices[0]["message"]["content"]

print(getEmoji("Whisperで文字起こしをした議事録の発話者の名前を自動的に判定する！"))

