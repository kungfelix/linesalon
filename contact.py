from line_bot_api import *

def contact_event(event):
    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/odz8hOx.jpg',
            title='Contact',
            text='我們誠摯地等待您的聯絡!',
            actions=[
                URIAction(
                    label='Call Us',
                    uri='tel:+886227580248'
                )
            ]
        )
    )

    line_bot_api.reply_message(
        reply_token=event.reply_token,messages=[buttons_template_message]
    )