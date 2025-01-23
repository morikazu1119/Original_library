import requests
import os
import re
from IPython.core.ultratb import AutoFormattedTB
from IPython import get_ipython

chat_url = "https://slack.com/api/chat.postMessage"
file_url = "https://slack.com/api/files.upload"

class Slack:
    def __init__(self, token, channel):
        self.token = token
        self.channel = channel
        self.tb_handler = AutoFormattedTB(mode="Plain", color_scheme="Neutral", ostream=open(os.devnull, "w"))  # エラートレース取得用
        self.jupyter_preprocess()

    def send_msg(self, text):
        """Slackにメッセージを送信"""
        headers = {"Authorization": "Bearer " + self.token}
        data = {
            "channel": self.channel,
            "text": text
        }
        response = requests.post(chat_url, headers=headers, json=data)
        if not response.ok:
            print(f"Slack通知エラー: {response.status_code}, {response.text}")

    def send_file(self, file_path):
        """Slackにファイルを送信"""
        data = {
            "token": self.token,
            "channels": self.channel,
            "filename": os.path.basename(file_path),
            "title": os.path.basename(file_path)
        }
        files = {"file": open(file_path, "rb")}
        response = requests.post(file_url, data=data, files=files)
        if not response.ok:
            print(f"Slack通知エラー: {response.status_code}, {response.text}")

    def jupyter_preprocess(self):
        """Jupyter Notebook の最初に実行する関数."""
        itb = AutoFormattedTB(mode='Plain', tb_offset=1)

        def custom_exc(shell, etype, evalue, tb, tb_offset=None):
            # 例外が発生した場合の処理
            shell.showtraceback((etype, evalue, tb), tb_offset=tb_offset)

            # トレースバックのフォーマット
            stb = itb.structured_traceback(etype, evalue, tb)
            sstb = itb.stb2text(stb)

            # ANSIカラーコードを正規表現で削除
            readable_traceback = re.sub(r'\x1b\[[0-9;]*m', '', ''.join(sstb))

            # エラー内容を整理してSlackに通知
            formatted_traceback = f"Exception: {etype}\nMessage: {evalue}\nTraceback:\n{readable_traceback}"

            # Slack通知
            self.send_msg(f"ERROR: 例外が発生しました。\n```\n{formatted_traceback}\n```")

            return sstb

        # カスタムエラーハンドラーを設定
        get_ipython().set_custom_exc((Exception,), custom_exc)

