import os
import sys
from flask import Flask, request
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.rest import Client
from twilio.twiml.voice_response import Dial, VoiceResponse, Sip

ACCOUNT_SID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
API_KEY = 'SKXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
API_KEY_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
PUSH_CREDENTIAL_SID = 'CRXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
APP_SID = 'APXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

CALLER_ID = '+886 111 222 333'
IDENTITY = 'default_identity'

app = Flask(__name__)

@app.route('/accessToken', methods=['GET', 'POST'])
def token():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)

  push_credential_sid = os.environ.get("PUSH_CREDENTIAL_SID", PUSH_CREDENTIAL_SID)
  app_sid = os.environ.get("APP_SID", APP_SID)

  grant = VoiceGrant(
    push_credential_sid=push_credential_sid,
    outgoing_application_sid=app_sid
  )

  identity = request.values["identity"] \
          if request.values and request.values["identity"] else IDENTITY
  token = AccessToken(account_sid, api_key, api_key_secret, identity=identity)
  token.add_grant(grant)

  return token.to_jwt()

@app.route('/makeCall', methods=['GET', 'POST'])
def makeCall():

  to = request.values.get("to")
  To = request.values.get("To")
  From = request.values.get("From")

  resp = VoiceResponse()
  myDomain = '@william.sip.us1.twilio.com'

  if From.startswith('sip:0001'):
    To = To.split(':0989', 1)[1].split('@', 1)[0]
    if To == '0002':
        dial = Dial(caller_id='0001')
        destination = To + '@william.sip.us1.twilio.com'
        resp.say("Cool! David You have just made call from 3CX sip domain to 0002 sip domain!")
        dial.sip(destination)
        resp.append(dial)
    else:
        resp.say("Cool! Kevin You have just made call from 3CX sip domain to mobile APP!")
        resp.dial(callerId=CALLER_ID).client(To)

  elif From.startswith('sip:0002'):
    To = To.split(':', 1)[1].split('@', 1)[0]
    if To == '0001':
        dial = Dial(caller_id='0002')
        destination = To + '@william.sip.us1.twilio.com'
        resp.say("Cool! Hellen You have just made call from sip domain to sip domain!")
        dial.sip(destination)
        resp.append(dial)

    else:
        resp.say("Cool! Stary You have just made call from sip domain to mobile APP!")
        print(To)
        resp.dial(callerId=CALLER_ID).client(To)

  elif From.startswith('client:'):
    dial = Dial(caller_id=IDENTITY)

    if to == '0001' or to == '0002':
        destination = to + '@william.sip.us1.twilio.com'
        resp.say("Congratulations! Peter You have just made call from mobile APP to sip domain!")
        dial.sip(destination)
        resp.append(dial)
    else:
        resp.say("Congratulations! Victor You have just made call from mobile APP! to mobile APP!")
        resp.dial(callerId=CALLER_ID).client(to)
  else:
    resp.say("Oh No! Something wrong")

  print(resp)
  return str(resp)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
