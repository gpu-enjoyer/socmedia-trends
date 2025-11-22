
import asyncio
import json
from   os.path import dirname

from vkbottle                   import API
from vkbottle.exception_factory import VKAPIError

class ParserVk:
    log_info:    list[str]
    is_prepared: bool
    api:         API
    chat_names:  list[str]
    depth:       int
    dir_path:    str

    def __init__(self):
        self.log_info = []
        self.log_info.append("ParserVk.__init__()")
        self.is_prepared = False

    def set_fields(self, inp_path: str):
        self.log_info = []
        self.log_info.append(f"ParserVk.set_fields(\"{inp_path}\")")
        flag = True
        config = {}
        try:
            with open(inp_path) as inp_file:
                loaded_file = json.load(inp_file)
                if "vk" in loaded_file:
                    config = loaded_file['vk']
                else:
                    self.log_info.append(f"  'vk' key not found")
                    return
        except FileNotFoundError:
            self.log_info.append(f"  FileNotFoundError")
            return
        except json.JSONDecodeError:
            self.log_info.append(f"  JSONDecodeError")
            return
        self.dir_path = dirname(inp_path)
        if "api_token" in config:
            self.api = API(token=config["api_token"])
            masked = config["api_token"][:2] + '*' * (len(config["api_token"]) - 2)
            self.log_info.append(f"  api_token     = {masked}")
        else:
            self.log_info.append(f"  'api_token' not found")
            flag = False
        if "chat_names" in config:
            self.chat_names = config["chat_names"]
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

    async def parse_chat(self, name: str) -> list[str]:
        chat_msgs = []
        try:
            chat = await self.api.wall.get(domain=name, count=self.depth)
            for post in chat.items:
                if post.text:
                    chat_msgs.append(post.text)
        except VKAPIError as e:
            self.log_info.append(f"  VK Error [{name}]: {e.code} - {e.error_msg}")
        except Exception as e:
            self.log_info.append(f"  VK Unknown Error [{name}]: {e}")
        return chat_msgs

    async def parse(self) -> list[str]:
        tasks = []
        for name in self.chat_names:
            tasks.append(self.parse_chat(name))
        results = await asyncio.gather(*tasks)
        all_msgs = []
        for r in results: 
            all_msgs.extend(r)
        return all_msgs
