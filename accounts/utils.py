from twilio.rest import Client
import environ

env = environ.Env()
environ.Env.read_env()


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = env('TWILIO_ACCOUNT_SID')
auth_token = env('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def send_sms(user_code, mobile):
     message = client.messages \
                .create(
                     body=f"Hi! Your email and verification code is {user_code}.",
                     from_='+14846737900',
                     to=f'{mobile}')
     print(message.sid)

