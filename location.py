from line_bot_api import *

def location_event(event):
    title_text = 'Location'
    address_text = '東京都港区六本木5丁目18-20'
    latitude = 35.660765
    longitude = 139.734773
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(title=title_text, address=address_text, latitude=latitude, longitude=longitude))
        


