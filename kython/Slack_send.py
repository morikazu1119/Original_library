import requests
import os
from IPython.core.ultratb import AutoFormattedTB
from IPython import get_ipython

chat_url = "https://slack.com/api/chat.postMessage"
file_url = "https://slack.com/api/files.upload"

class Slack:
    def __init__(self, token, channel):
        self.token = token
        self.channel = channel
        self.tb_handler = AutoFormattedTB(mode="Plain", color_scheme="Neutral", ostream=open(os.devnull, "w"))  # エラートレース取得用

    def __call__(self, *args, **kwargs):
        # エラーが発生した場合にSlackへ送信
        ipython = get_ipython()
        if ipython is not None:
            exc_type, exc_value, tb = ipython._last_traceback
            if exc_value is not None:
                error_msg = self.tb_handler.text(*args)  # エラーメッセージを文字列として取得
                self.send_msg(f"Error occurred in Jupyter Notebook:\n```\n{error_msg}\n```")

    def send_msg(self, text):
        headers = {"Authorization": "Bearer " + self.token}
        data = {
            "token": self.token,
            "channel": self.channel,
            "text": text
        }
        response = requests.post(chat_url, headers=headers, data=data)
        #print(response.json())

    def send_file(self, file_path):
        data = {
            "token": self.token,
            "channels": self.channel,
            "filename": os.path.basename(file_path),
            "title": os.path.basename(file_path)
        }
        files = {"file": open(file_path, "rb")}
        response = requests.post(file_url, data=data, files=files)
        #print(response.json())
