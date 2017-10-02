from twilio.rest import Client

account_sid = "AC6cb913ea9cc19bf3b95733f5a2989ec1"
auth_token = "7aa1695cf449042b3426c8aa5dfe056e"
client = Client(account_sid, auth_token)


def send_message(body, phone_number):
    message = client.messages.create(
        to=phone_number,
        from_="+12166000727",
        body=body)

    return message.sid
