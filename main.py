import smtplib
import ssl
from fastapi import FastAPI, Query, HTTPException
from pydantic import EmailStr

app = FastAPI()

port = 587  # For starttls
smtp_server = "smtp.outlook.com"
sender_email = "deneme_test_ety@outlook.com"
password = "123?test}567"


def send_email(receiver_email, message):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

#It should be post method, but since I got it from the url, it did not allow the post method.
@app.get("/send_email/", summary="Send an email", description="Send an email to the specified email address.")
async def send_email_endpoint(
        receiver_email: EmailStr = Query(..., title="Receiver Email", description="Email address of the receiver.")
):
    """
    Send an email to the specified email address.

    :param receiver_email: Email address of the receiver.
    :return: {"message": "Email sent successfully!"}
    """
    subject = "Hi there"
    email_message = f"Subject: {subject}\n\nThis message is sent from Beyza Kercek."
    email_message_utf8 = email_message.encode('utf-8')

    send_email(receiver_email, email_message_utf8)
    return {"message": "Email sent successfully!"}
