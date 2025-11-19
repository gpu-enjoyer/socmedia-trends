
import json

class ParserTg:
    log:        list[str]
    is_empty:   bool
    api_id:     str
    api_hash:   str
    chat_names: list[str]
    depth:      int

    def __init__(self, inp_path: str):
        self.log = []
        self.log.append(f"ParserTg(\"{inp_path}\")")
        self.is_empty = True
        conf = {}
        try:
            with open(inp_path) as inp_file:
                loaded_file = json.load(inp_file)
                if "tg" in loaded_file:
                    conf = loaded_file['tg']
                    self.is_empty = False
                else:
                    self.log.append(f"  'tg' key not found - won't be parsed!")
                    return
        except FileNotFoundError:
            self.log.append(f"  FileNotFoundError")
            return
        except json.JSONDecodeError:
            self.log.append(f"  JSONDecodeError")
            return
        if "api_id" in conf:
            self.api_id = str(conf["api_id"])
            masked = self.api_id[:2] + '*' * (len(self.api_id) - 2)
            self.log.append(f"  api_id = {masked}")
        else:
            self.log.append(f"  'api_id' not found")
        if "api_hash" in conf:
            self.api_hash = str(conf["api_hash"])
            masked = self.api_hash[:3] + '*' * (len(self.api_hash) - 3)
            self.log.append(f"  api_hash = {masked}")
        else:
            self.log.append(f"  'api_hash' not found")
        if "chat_names" in conf:
            self.chat_names = list[str](conf["chat_names"])
            self.log.append(f"  chat_names = [{self.chat_names[0]}, ...]")
        else:
            self.log.append(f"  'chat_names' not found")
        if "depth" in conf:
            self.depth = int(conf["depth"])
            self.log.append(f"  depth = {self.depth}")
        else:
            self.log.append(f"  'depth' not found")

