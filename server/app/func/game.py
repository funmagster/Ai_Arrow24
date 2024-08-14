from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from prompts import prompts
import os
from dotenv import load_dotenv

import json
import asyncio

import re
import requests

import base64
from PIL import Image
from io import BytesIO


class ObozLLM:
    def __init__(self):
        load_dotenv()
        self.url_kandinsky = "https://api-key.fusionbrain.ai/"
        self.AUTH_HEADERS_kandinsky = {
            'X-Key': f'Key {os.getenv("API_kandinsky")}',
            'X-Secret': f'Secret {os.getenv("Secret_key_API_kandinsky")}',
        }
        self.llm_model = GigaChat(
                credentials=os.getenv('CREADENTIALS_gigachat'),
                model='GigaChat',
                verify_ssl_certs=False
        )

    async def get_story(self, prompt: str):
        messages = [
            SystemMessage(
                content=prompts["who you are"]
            ),
            HumanMessage(content=prompts["story"] + prompt)
        ]
        return self.llm_model(messages).content

    async def get_model(self):
        response = requests.get(self.url_kandinsky + 'key/api/v1/models', headers=self.AUTH_HEADERS_kandinsky)
        data = response.json()
        return data[0]['id']

    async def generate(self, prompt, model, images=1, width=1024, height=576):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.url_kandinsky + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS_kandinsky, files=data)
        data = response.json()
        return data['uuid']

    async def check_generation(self, request_id, attempts=120, delay=2):
        while attempts > 0:
            response = requests.get(self.url_kandinsky + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS_kandinsky)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images'][0]

            attempts -= 1
            await asyncio.sleep(delay)
        return None

    async def get_img(self, prompt):
        model_id = await self.get_model()
        uuid = await self.generate(prompt, model_id)
        image = await self.check_generation(uuid)
        return image

    async def get_prompt_img(self, description):
        messages = [
            SystemMessage(
                content=prompts["system generated img"]
            ),
            HumanMessage(content=prompts["generates img"] + description)
        ]
        return self.llm_model(messages).content

    async def get_character(self, count_characters, story):
        messages = [
            SystemMessage(
                content=prompts["who you are"]
            ),
            HumanMessage(content=prompts["character generation"].format(count_characters, story))
        ]
        return self.llm_model(messages).content

    async def get_play(self, count_room_complete, history, story, character, prompt):
        messages = [
            SystemMessage(
                content=prompts["who you are in the play"]
            ),
            HumanMessage(content=prompts["play"].format(count_room_complete, story, history, character, prompt))
        ]
        return self.llm_model(messages).content


def split_story(text):
    matches = pattern.findall(text)
    result = [match[1].strip() for match in matches]
    return result


def split_characters(text):
    return text.split('\n\n')


async def image_to_base64(image_path, format):

    with Image.open(image_path) as image:
        buffered = BytesIO()
        image.save(buffered, format=format)
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return img_base64


def get_json_format(json_str):
    return json.loads(json_str)


oboz_LLM = ObozLLM()
pattern = re.compile(r'(Завязка|Основной конфликт|Кульминация|Развязка):\s*(.*?)(?=\n(?:Завязка|Основной конфликт|Кульминация|Развязка):|\Z)', re.DOTALL)
