# -*- coding: utf-8 -*-

import openai

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
	#print(response.choices[0].message.content)
	return response.choices[0].message.content

def makeEmoji(title):
	gpt_model_name = "gpt-4"
	dall_model_name = "dall-e-3"

	print(title)
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
	print("prompt:" + image_prompt.choices[0].message.content)
	print("レジギ、ガガガガガwww")
	response = openai.images.generate(
		model=dall_model_name,
		prompt=image_prompt.choices[0].message.content + ",simple,anime,Emoji",
		size="1024x1024",
		quality="standard",
		n=1,
	)
	image_url = response.data[0].url
	print(image_url)

#print(getEmoji("Whisperで文字起こしをした議事録の発話者の名前を自動的に判定する！",[]))
makeEmoji("Whisperで文字起こしをした議事録の発話者の名前を自動的に判定する！")


