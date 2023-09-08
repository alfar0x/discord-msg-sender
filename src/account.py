import json
import requests

from src.logger import logging

logger = logging.getLogger(f"discord_account")


class Account:
    def __init__(self, token: str, proxy: str, user_agent: str, chat_id: int | str):
        self.token = token
        self.proxy = proxy
        self.user_agent = user_agent
        self.chat_id = chat_id
        self.session = self.__create_account_session()

    def __create_account_session(self):
        session = requests.Session()

        session.headers = {"user-agent": self.user_agent, "authorization": self.token}
        session.proxies = {"http": self.proxy, "https": self.proxy}

        return session

    def check_chat_access(self):
        url = f"https://discord.com/api/v9/channels/{self.chat_id}/messages?limit=2"
        response = self.session.get(url)

        if response.status_code != 200:
            raise Exception(f"check chat access status code is {response.status_code}")

    def send_message(self, message: str) -> dict:
        data = {"content": message, "tts": False}
        url = f"https://discord.com/api/v9/channels/{self.chat_id}/messages"
        response = self.session.post(url, json=data)

        if response.status_code != 200:
            raise Exception(f"send message status code is {response.status_code}")

        return json.loads(response.text)
