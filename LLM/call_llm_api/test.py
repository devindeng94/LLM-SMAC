# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI


client = OpenAI(api_key="Your API key here.",
                base_url="Base URL here.")
print("start")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
