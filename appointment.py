from line_bot_api import *
from urllib.parse import parse_qsl
import datetime


def appointment_event(event):
    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/EnaVHNt.jpg',
                    title='剪髮與髮型設計',
                    text='請選擇服務',
                    actions=[
                        PostbackAction(
                            label='洗頭與吹乾',
                            text='洗頭與吹乾',
                            data='action=step2&service=洗頭與吹乾'
                        ),
                        PostbackAction(
                            label='Dry Haircut & Style',
                            text='Dry Haircut & Style',
                            data='action=step2&service=Dry Haircut and Style'
                        ),
                        PostbackAction(
                            label='Wash Hair & Style',
                            text='Wash Hair & Style',
                            data='action=step2&service=Wash Hair and Style'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/GVCut9a.jpg',
                    title='Massage',
                    text='Select Service',
                    actions=[
                        PostbackAction(
                            label='Foot Massage',
                            text='Foot Massage',
                            data='action=step2&service=Foot Massage'
                        ),
                        PostbackAction(
                            label='De-Stress Massage',
                            text='De-Stress Massage',
                            data='action=step2&service=De-Stress Massage'
                        ),
                        PostbackAction(
                            label='Deep Tissue Massage',
                            text='Deep Tissue Massage',
                            data='action=step2&service=Deep Tissue Massage'
                        )
                    ]
                )
            ]
        )
    )

    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=[TextSendMessage(text='Which service would you like to book?'),
                  carousel_template_message]
    )


def appointment_datetime_event(event):
    data = dict(parse_qsl(event.postback.data))

    now = datetime.datetime.now()
    min_date = now + datetime.timedelta(days=2)
    max_date = now + datetime.timedelta(days=9)
    image_carousel_template_message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/ocEs29U.jpg',
                    action=DatetimePickerAction(
                        label="預約時間",
                        data="action=step3&service={}".format(data.get('service')),
                        mode="datetime",
                        initial=min_date.strftime('%Y-%m-%dT00:00'),
                        min=min_date.strftime('%Y-%m-%dT00:00'),
                        max=max_date.strftime('%Y-%m-%dT23:59')
                    )
                )
            ]
        )
    )

    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=[image_carousel_template_message]
    )


def appointment_completed_event(event):
    appointment_service = dict(parse_qsl(event.postback.data)).get('service')
    appointment_datetime = datetime.datetime.strptime(event.postback.params.get('datetime'), '%Y-%m-%dT%H:%M')
    profile_name = line_bot_api.get_profile(event.source.user_id).display_name
    appointment_service_text = 'Thanks {name}! You\'re book in for a {service}'.format(name=profile_name,
                                                                                       service=appointment_service)
    appointment_datetime_text = appointment_datetime.strftime('Your appointment date is %Y-%m-%d, and the time is %H:%M')

    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=[TextSendMessage(text=appointment_service_text),
                  TextSendMessage(text=appointment_datetime_text)]
    )