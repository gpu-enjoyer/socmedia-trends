
import asyncio
import json
from   os.path import dirname
from   pyrogram.client import Client
from   pyrogram.types  import Chat


class ParserTg:
    log_info:    list[str]
    is_prepared: bool
    api_id:      str
    api_hash:    str
    chat_names:  list[str]
    depth:       int
    dir_path:    str

    def __init__(self):
        self.log_info = []
        self.log_info.append("Parser.__init__()")
        self.is_prepared = False

    def set_fields(self, inp_path: str):
        self.log_info = []
        self.log_info.append(f"Parser.set_fields(\"{inp_path}\")")
        flag = True
        config = {}
        try:
            with open(inp_path) as inp_file:
                loaded_file = json.load(inp_file)
                if "tg" in loaded_file:
                    config = loaded_file['tg']
                else:
                    self.log_info.append(f"  'tg' key not found")
                    return
        except FileNotFoundError:
            self.log_info.append(f"  FileNotFoundError")
            return
        except json.JSONDecodeError:
            self.log_info.append(f"  JSONDecodeError")
            return
        self.dir_path = dirname(inp_path)
        if "api_id" in config:
            self.api_id = str(config["api_id"])
            masked = self.api_id[:1] + '*' * (len(self.api_id) - 1)
            self.log_info.append(f"  api_id     = {masked}")
        else:
            self.log_info.append(f"  'api_id' not found")
            flag = False
        if "api_hash" in config:
            self.api_hash = str(config["api_hash"])
            masked = self.api_hash[:2] + '*' * (len(self.api_hash) - 2)
            self.log_info.append(f"  api_hash   = {masked}")
        else:
            self.log_info.append(f"  'api_hash' not found")
            flag = False
        if "chat_names" in config:
            self.chat_names = ['@' + n for n in config["chat_names"]]
            self.log_info.append(f"  chat_names = [{self.chat_names[0]}, ...]")
        else:
            self.log_info.append(f"  'chat_names' not found")
            flag = False
        if "depth" in config:
            self.depth = int(config["depth"])
            self.log_info.append(f"  depth      = {self.depth}")
        else:
            self.log_info.append(f"  'depth' not found")
        self.is_prepared = self.is_prepared or flag

    async def parse_chat(self, client: Client, name: str):
        chat_msgs = []
        try:
            chat = await client.get_chat(name)
            if not isinstance(chat, Chat):
                self.log_info.append(f"  channel '{name}': unavailable")
                return chat_msgs
            async for msg in client.get_chat_history(chat.id, limit=self.depth): #type:ignore
                chat_msgs.append(msg.text or msg.caption or '')
        except Exception as e:
            self.log_info.append(f"  channel '{name}': error {e}")
        return chat_msgs

    async def parse(self) -> list[str]:
        all_msgs = []
        tasks = []
        async with Client(name="tg", workdir=self.dir_path,
        api_id=self.api_id, api_hash=self.api_hash)\
        as client:
            for chat_name in self.chat_names:
                coro = self.parse_chat(client, chat_name)
                tasks.append(asyncio.create_task(coro))
            results = await asyncio.gather(*tasks)
        for r in results: all_msgs.extend(r)
        return all_msgs
