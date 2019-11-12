from flask import Flask
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)


@app.route("/record", methods=['GET', 'POST'])
def record():
    # """Returns TwiML which prompts the caller to record a message"""
    # # Start our TwiML response
    # response = VoiceResponse()
    #
    # # Use <Say> to give the caller some instructions
    # response.say('Hello. Please leave a message after the beep.')
    #
    # # Use <Record> to record the caller's message
    # response.record()
    #
    # # End the call with <Hangup>
    # response.hangup()

    response = VoiceResponse()
    response.say('How are you fatty?', voice='woman', loop=1)
    # print(response)

    return str(response)

if __name__ == "__main__":
    app.run()

