
import asyncio
import json
import requests # TODO
from   pyrogram.client import Client
from   pyrogram.types  import Chat


class DataParser:
    def __init__(self):
        self.tg_chat_names  = []  #  <- GUI
        self.tg_depth       = 10  # todo: GUI
        self.vk_chat_ids    = []  #  <- GUI
        self.vk_depth       = 10  # todo: GUI
        self.tokens         = self.get_tokens("input/tokens.json")

    def get_tokens(self, tokens_path: str) -> dict:
        tokens = {}
        try:
            with open(tokens_path) as tokens_file:
                tokens = json.load(tokens_file) 
        except FileNotFoundError:
            print(f"ERROR: {tokens_path} not found")
        except json.JSONDecodeError:
            print(f"ERROR: {tokens_path} json decode error")
        return tokens

    async def tg_parse_chat(self, client: Client, name: str):
        chat_msgs = []
        try:
            chat = await client.get_chat(name)
            if not isinstance(chat, Chat):
                print(f"telegram: channel '{name}': unavailable")
                return chat_msgs
            chat_history = await client.get_chat_history(chat.id, limit=self.tg_depth)
            if chat_history:
                async for msg in chat_history:
                    chat_msgs.append(msg.caption or msg.text or '')
        except Exception as e:
            print(f"telegram: channel '{name}': error {e}")
        return chat_msgs

    # TODO what does it return?
    async def tg_parse(self):
        tasks = []
        client = Client(
            name     = "tg",
            workdir  = "../output/",
            api_id   = self.tokens["tg"]["api_id"],
            api_hash = self.tokens["tg"]["api_hash"])
        async with client:
            for chat_name in self.tg_chat_names:
                tasks.append(self.tg_parse_chat(client, chat_name))
        return asyncio.run(self.tg_parse())        

    # TODO async
    def vk(self):
        all_msgs  = []
        for chat_id in self.vk_chat_ids:
            response = requests.get(
                'https://api.vk.com/method/wall.get',
                params={
                    'access_token': self.tokens["vk"]["api"],
                    'v':            '5.131',
                    'owner_id':     int(chat_id),
                    'count':        self.vk_depth
                }
            ).json()
            for item in response['response']['items']:
                all_msgs.append(item.get('text', ''))
        return all_msgs
