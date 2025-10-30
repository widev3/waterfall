import json


class Config:
    _instance = None

    def __new__(cls, conf=None):
        if cls._instance is None:
            if conf:
                cls._instance = super(Config, cls).__new__(cls)
            else:
                raise Exception("Cannot instance without a configuration file")
        elif conf:
            raise Exception("Dynamic configuration file is not implemented")

        return cls._instance

    def __init__(self, conf=None):
        if not hasattr(self, "initialized"):
            if not conf:
                raise Exception("Cannot instance without a configuration file")

            with open(conf, "r") as f:
                self.config = json.load(f)

            self.initialized = True
