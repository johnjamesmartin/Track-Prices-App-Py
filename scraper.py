# Dependencies:
import requests
from bs4 import BeautifulSoup
import smtplib
import time


# URL for "Sapiens" book on Amazon:
URL = 'https://www.amazon.co.uk/Sapiens-Humankind-Yuval-Noah-Harari/dp/0099590085/ref=sr_1_1?keywords=sapiens&qid=1564272796&s=gateway&sr=8-1'
# If less than 6 GBP, send email:
NOTIFICATION_PRICE = 6.00
# Send this as the subject line:
NOTIFICATION_EMAIL_SUBJECT = "Sapiens book has fallen in price!"
# Check every 1440 seconds (daily)
NOTIFICATION_CHECK_RATE = 1440

# Set header for user agent. Replace user agent with your own:
headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}


# Check price function:
def check_price():
    page = requests.get(URL, headers=headers)
    # Use soup function twice to "trick" Amazon (which uses JS to generate HTML):
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    # Set variables from extracted HTML elements:
    title = soup2.find(id="productTitle").get_text().strip()
    price = soup2.find("span", class_="a-color-price").get_text().strip()
    # Format price:
    converted_price = float(price[1:5])
    # Check if price is below notification price
    if (converted_price < NOTIFICATION_PRICE):
      send_email()
    # Print title and price:
    print(title)
    print(converted_price)


# Send email function:
def send_email():
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()
  # Gmail (has to be two-step verified)
  # Set up Google app to work for email and paste below
  server.login("YOUR_GMAIL@GMAIL.COM", "YOUR_GOOGLE_APP_GENERATED_PASSWORD")
  subject = NOTIFICATION_EMAIL_SUBJECT
  body = "Check out the Amazon link: https://www.amazon.co.uk/Sapiens-Humankind-Yuval-Noah-Harari/dp/0099590085/ref=sr_1_1?keywords=sapiens&qid=1564272796&s=gateway&sr=8-1"
  msg = "Subject: " + subject + "\n\n" + body
  server.sendmail(
    "EMAIL_ADDRESS_TO_SEND_NOTIFICATION_TO_1@EMAIL.COM",
    "EMAIL_ADDRESS_TO_SEND_NOTIFICATION_TO_2@EMAIL.COM",
    msg
  )
  print("Successfully sent email")
  server.quit()


while(True):
  check_price()
  time.sleep(NOTIFICATION_CHECK_RATE)