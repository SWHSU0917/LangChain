import os

from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from langchain_openai import ChatOpenAI
from langchain.schema.messages import SystemMessage, HumanMessage

app = Flask(__name__)

# 載入環境變數
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 用 OpenAI 新版 SDK 初始化 client，整合所有參數
model = ChatOpenAI(
  model = OPENAI_API_MODEL,
  openai_api_key = OPENAI_API_KEY,
  openai_api_base = "https://free.v36.cm/v1/",
  default_headers = {"x-foo": "true"}
)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return "OK"

# messages = [
#     SystemMessage(content="請你一律用繁體中文回答以下問題。"),
#     HumanMessage(content="")
# ]

@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):

    messages = [
        SystemMessage(content="請你一律用繁體中文回答以下問題。"),
        HumanMessage(content=event.message.text)
    ]
    #messages[1].content = event.message.text

    # LangChain 產生回覆（這裡固定回答）
    response = model.invoke(messages)

    # 回覆LINE用戶
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response.content)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="8080")
