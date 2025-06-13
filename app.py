import os

from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from ollama_llm import OllamaLLM

app = Flask(__name__)

# 載入環境變數
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

model = OllamaLLM(
    api_url = "http://ollama-swhsu0917-dev.apps.rm2.thpm.p1.openshiftapps.com",
    model = "llama3.2:1b"
)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):

    question = event.message.text

    prompt = f"請一律使用繁體中文回答以下問題：\n{question}"
    response = model._call(prompt)

    # 回覆LINE用戶
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="8080")
