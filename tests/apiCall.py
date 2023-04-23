import openai
openai.api_key = "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"

prompt = "Hello, ChatGPT!"
model = "text-davinci-002"
response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=50)

print(response.choices[0].text.strip())
