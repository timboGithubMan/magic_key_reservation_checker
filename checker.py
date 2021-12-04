#!/usr/bin/env python3
import datetime
import sys
import time
import requests
import smtplib
from email.message import EmailMessage

# change "enchant-key-pass" in URL to "imagine-key-pass" etc for whatever pass you have
# change it to "dream-key-pass" to view regular availability (dream key pass has no blockout dates - same as regular tickets)

URL = 'https://disneyland.disney.go.com/passes/blockout-dates/api/get-availability/?product-types=enchant-key-pass&numMonths=2'

# you might have to change the email server in the while loop below if youre not using gmail (smtplib.SMTP_SSL('smtp.gmail.com', 465))

sender_email = "yourEmail@gmail.com"
sender_password = "yourPassword"

recipient_email = "recipient@gmail.com"

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 1, 30)


def main():
    resp = requests.get(URL, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    })
    if resp.status_code != 200:
        sys.exit(1)
    results = resp.json()["calendar-availabilities"]

    while True:
        for result in results:
            date = datetime.date.fromisoformat(result["date"])
            if end_date >= date >= start_date:
                if result["availability"] != "cms-key-no-availability":
                    print(result["date"])
                    msg = EmailMessage()
                    msg.set_content(result["date"])

                    msg['Subject'] = (result["date"] + " disney reservation")
                    msg['From'] = sender_email
                    msg['To'] = recipient_email

                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                    server.quit()

                    print("Email sent successfully!")

                    time.sleep(120)
                    sys.exit()
        print("sleep")
        time.sleep(60)

    print("ok")


if __name__ == '__main__':
    main()
