import json

class Config:
    def __init__(self):
        with open('config.json', 'r', encoding='UTF-8') as f:
            self._config: dict = json.load(f)

    def __getitem__(self, key: str):
        return self._config[key]

    def save(self):
        with open('config.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(self._config))

    def set(self, key: str, value):
        self._config[key] = value
        self.save()

config = Config()