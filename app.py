import os
from flask import Flask, render_template, request, url_for, Response
import openai
import requests
from twilio.rest import Client

app = Flask(__name__)
AUDIO_FILE = 'static/generated.mp3'

openai.api_key = os.environ.get('OPENAI_API_KEY')
ELEVEN_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_AUTH = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

client = Client(TWILIO_SID, TWILIO_AUTH)

RECIPIENT_SMS = ['+15551234567']
RECIPIENT_CALL = ['+15557654321']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['message']
        completion = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        text = completion['choices'][0]['message']['content'].strip()
        audio_bytes = generate_audio(text)
        with open(AUDIO_FILE, 'wb') as f:
            f.write(audio_bytes)
        return render_template('approve.html', text=text, audio=url_for('static', filename='generated.mp3'))
    return render_template('index.html')


def generate_audio(text: str) -> bytes:
    resp = requests.post(
        'https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL',
        headers={
            'xi-api-key': ELEVEN_API_KEY,
            'Content-Type': 'application/json'
        },
        json={'text': text}
    )
    return resp.content


@app.route('/send', methods=['POST'])
def send():
    text = request.form['text']
    for to in RECIPIENT_SMS:
        client.messages.create(body=text, from_=TWILIO_NUMBER, to=to)
    twiml_url = url_for('twiml', _external=True)
    for to in RECIPIENT_CALL:
        client.calls.create(to=to, from_=TWILIO_NUMBER, url=twiml_url)
    return 'Messages sent.'


@app.route('/twiml', methods=['GET', 'POST'])
def twiml():
    audio_url = url_for('static', filename='generated.mp3', _external=True)
    xml = f"<?xml version='1.0' encoding='UTF-8'?><Response><Play>{audio_url}</Play></Response>"
    return Response(xml, mimetype='text/xml')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
