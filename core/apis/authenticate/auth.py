from werkzeug.security import generate_password_hash
from datetime import datetime,timedelta
import jwt,os,random
from core.libs.assertions import assert_found,assert_valid
from twilio.rest import Client

def GenPasswordHash(password):
    return generate_password_hash(password)

def Gen(payload, secret_key):
    return jwt.encode(payload, secret_key, algorithm='HS256')

def SetTime(time):
    time=datetime.now()+timedelta(minutes=time)
    return int(time.timestamp())

def TransformData(data):
    dob_str = data['user']['dob'].isoformat()
    return {
        "user": {
            "name": data['user']['name'].lower(),
            "gender": data['user']['gender'].lower(),
            "dob": dob_str,
            "mobile": data['user']['mobile']
        },
        "username": {
            "email": data['username']['email'].lower(),
            "password": GenPasswordHash(data['username']['password'])
        }
    }

def GenToken(data, type, no):
    exp_time=SetTime(15)
    payload={"data":data, "type":type, "expire": exp_time}
    return Gen(payload, str(GenOtp(no)))

def Decript(token, secret_key):
    try:
        payload=jwt.decode(token, str(secret_key['otp']),algorithms=['HS256'])
    except:
        assert_found(None,'please enter correct otp')
    assert_valid(payload['expire']>int(datetime.now().timestamp()),"otp has been expired !!!")
    return payload

def Authorization(email):   #used for login
    exp_time=SetTime(60)
    payload={"email":email,"expire":exp_time}
    return Gen(payload,os.getenv('authorization_secret_key'))

def Decrept_email(token):
    try:
        payload=jwt.decode(token,os.getenv('authorization_secret_key'),algorithms=['HS256'])
    except:
        assert_found(None,"Don't do this anymore")
    assert_valid(payload['expire']>int(datetime.now().timestamp()),"token has been expired !!!")
    return payload['email']

def GenOtp(no):
    otp=random.randint(1000,9999)
    print(otp)
    SendOtp("+91"+f"{no}", otp)
    return otp

def SendOtp(no,otp):

    try:
        client = Client('ACb6a39fb9ab31679e5e6b6bfad0eb2c27', '318c85e9f36ca0fca852969f86db713e')

        message = client.messages.create(
            from_="+14843024845",
            body= f"this otp {otp} is for verification",
            to=no
        )

        # Return message SID if successful
        return message.sid
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return None








# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def send_email():
#     sender_email = 'rishav@bengalinstituteoftechnology.online'
#     receiver_email = 'rishavghosh147@gmail.com'
#     subject = 'Test Email'
#     body = 'Hello, this is a test email sent from my custom SMTP server!'

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))

#     with smtplib.SMTP('0.0.0.0', 25) as server:
#         server.sendmail(sender_email, receiver_email, msg.as_string())

# Call the function to send the email
# send_email()

# Keep the event loop running
# asyncio.get_event_loop().run_forever()
