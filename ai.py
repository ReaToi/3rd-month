from decouple import config
import openai

openai.api_key = config('OPENAI_API_KEY')


def get_text(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']


def image_generation(message):
    response = openai.Image.create(
        prompt=message.text,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']
