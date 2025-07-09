import os
import json

class ConfigReader:
    _config = None

    @staticmethod
    def load_config():
        if ConfigReader._config is None:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'testsetting.json')
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            with open(config_path, 'r', encoding='utf-8') as file:
                ConfigReader._config = json.load(file)
        return ConfigReader._config
        

    @staticmethod
    def get_base_url():
        return ConfigReader.load_config()['url']
    
    @staticmethod
    def get_username():
        return ConfigReader.load_config()['user']
    @staticmethod
    def get_password():
        return ConfigReader.load_config()['pass']