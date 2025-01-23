# Original_library (Python)

## Contain

kython
- Slack_send.py
  - send msg, send file and send error log

## Sample Code
```
import sys
sys.path.append("{your parent dir}")
from kython import Slack

token="{your token}"
channel="{channel name}"

slack = Slack(token=token, channel=channel)
slack.send_msg("Hello, world!")
```

## Coming soon

- send a message to Line (if your problem has error in jupyter notebook and so on.)
