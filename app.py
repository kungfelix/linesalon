from flask import Flask, request, abort

from urllib.parse import parse_qsl
from line_bot_api import *
from database import db_session, init_db
from about_us import about_us_event
from location import location_event
from contact import contact_event
from appointment import appointment_event, appointment_datetime_event, appointment_completed_event
from models.users import User

app = Flask(__name__)

@app.before_first_request
def init():
    init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

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
    user_id = event.source.user_id

    user = User.query.filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id)
        db_session.add(user)
        db_session.commit()

    if message_text == '@aboutus':
        about_us_event(event)

    elif message_text == '@location':
        location_event(event)

    elif message_text == '@contact':
        contact_event(event)

    elif message_text == '@booknow':
        appointment_event(event)


@handler.add(PostbackEvent)
def handle_postback(event):
    data = dict(parse_qsl(event.postback.data))

    if data.get('action') == 'step2':
        appointment_datetime_event(event)
    if data.get('action') == 'step3':
        appointment_completed_event(event)



#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
