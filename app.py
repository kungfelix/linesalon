from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('2/n0t/0MwQdeizWWKw/hE+bSlBDWt3JcfVPiSkt+lSFUJJQsdgT1b0/99tb2N69bGaCN8ELaMOlGv4yhA3yL5xrop+YM8nzVDmeLfYEnppxKz0/MGhMk3IkuSwXMV4FTeNSUYVM8Q+Ek5fSehKn/7wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('61a79162dbaf371ae9160a8a9d5a66b3')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()

    if message_text == '@aboutus':
        about_us_text = '我們是Line Salon，提供專業與尊榮的服務，敬請多多指教!'
        about_us_image = 'https://i.imgur.com/hyhgryf.jpg'
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=about_us_text),
             ImageSendMessage(original_content_url=about_us_image, preview_image_url=about_us_image),
             StickerSendMessage(package_id=2, sticker_id=28)])

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
