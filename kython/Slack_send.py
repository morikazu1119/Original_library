def set_token_channel(tok,chan):
  global token
  token=tok
  global channel
  channel=chan

def slack_msg(text):

  import requests
  url = "https://slack.com/api/chat.postMessage"
  headers = {"Authorization": "Bearer " + token}

  data={
      "token": token,
      "channel": channel,
      "text": text
  }

  response=requests.post(url,headers=headers,data=data)
  #print(response.json())

def slack_file(file_path):

  import requests
  import os
  url="https://slack.com/api/files.upload"

  data={
      "token": token,
      "channels": channel,
      "filename": os.path.basename(file_path),
      "title": os.path.basename(file_path)
  }
  files={"file": open(file_path, "rb")}

  response=requests.post(url, data=data, files=files)
  #print(response.json())