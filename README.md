# A4C Phone Tree

Simple Flask application demonstrating a phone tree that uses ChatGPT to draft a message, ElevenLabs to generate audio, and Twilio to deliver SMS and voice calls.

## Setup

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Export required credentials:

```
export OPENAI_API_KEY=your_openai_key
export ELEVENLABS_API_KEY=your_elevenlabs_key
export TWILIO_SID=your_twilio_sid
export TWILIO_AUTH_TOKEN=your_twilio_auth_token
export TWILIO_NUMBER=+15551234567
```

3. Adjust the recipient lists in `app.py` (`RECIPIENT_SMS` and `RECIPIENT_CALL`).

4. Run the app:

```
python app.py
```

The application will be available at `http://localhost:5000`.
