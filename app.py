import os
from dotenv import load_dotenv

# Loads variables from a .env file in the project root into os.environ.
# This must run before anything reads os.environ for credentials.
load_dotenv()

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

# Load Twilio credentials from environment variables — never hardcode these.
ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = os.environ["TWILIO_PHONE_NUMBER"]

# Twilio REST client used to send outbound messages.
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)


@app.route("/sms", methods=["POST"])
def incoming_sms():
    # Twilio sends the sender's message body as a form field called "Body".
    incoming_body = request.form.get("Body", "")

    # TwiML (Twilio Markup Language) is how you tell Twilio what to reply.
    response = MessagingResponse()
    response.message(f"Hi! I received your message: {incoming_body}")

    # Flask must return the TwiML as XML with the correct content type.
    return str(response), 200, {"Content-Type": "application/xml"}


def send_sms(to_number: str, message: str) -> str:
    """Send an outbound SMS and return the message SID."""
    msg = twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=to_number,
    )
    return msg.sid


if __name__ == "__main__":
    # Run with debug=False in production.
    app.run(debug=True, port=5000)
