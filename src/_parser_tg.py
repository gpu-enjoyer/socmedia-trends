
import json

class ParserTg:
    log:         list[str]
    is_prepared: bool
    api_id:      str
    api_hash:    str
    chat_names:  list[str]
    depth:       int

    def __init__(self):
        self.log = []
        self.log.append(f"ParserTg()")
        self.is_prepared = False

    def set_fields(self, inp_path: str):
        self.log = []
        self.log.append(f"ParserTg.set_fields(\"{inp_path}\")")
        flag = True
        config = {}
        try:
            with open(inp_path) as inp_file:
                loaded_file = json.load(inp_file)
                if "tg" in loaded_file:
                    config = loaded_file['tg']
                else:
                    self.log.append(f"  'tg' key not found")
                    return
        except FileNotFoundError:
            self.log.append(f"  FileNotFoundError")
            return
        except json.JSONDecodeError:
            self.log.append(f"  JSONDecodeError")
            return
        if "api_id" in config:
            self.api_id = str(config["api_id"])
            masked = self.api_id[:2] + '*' * (len(self.api_id) - 2)
            self.log.append(f"  api_id     = {masked}")
        else:
            self.log.append(f"  'api_id' not found")
            flag = False
        if "api_hash" in config:
            self.api_hash = str(config["api_hash"])
            masked = self.api_hash[:3] + '*' * (len(self.api_hash) - 3)
            self.log.append(f"  api_hash   = {masked}")
        else:
            self.log.append(f"  'api_hash' not found")
            flag = False
        if "chat_names" in config:
            self.chat_names = list(config["chat_names"])
            self.log.append(f"  chat_names = [{self.chat_names[0]}, ...]")
        else:
            self.log.append(f"  'chat_names' not found")
            flag = False
        if "depth" in config:
            self.depth = int(config["depth"])
            self.log.append(f"  depth      = {self.depth}")
        else:
            self.log.append(f"  'depth' not found")
        # ready to try connection
        self.is_prepared = self.is_prepared or flag

    def connect(self):
        pass
