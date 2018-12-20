from line_bot_api import *


def about_us_event(event):
    about_us_text = '我們是Line Salon，提供專業與尊榮的服務，敬請多多指教!'
    about_us_image = 'https://i.imgur.com/hyhgryf.jpg'
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=about_us_text),
         ImageSendMessage(original_content_url=about_us_image, preview_image_url=about_us_image),
         StickerSendMessage(package_id=2, sticker_id=28)])
