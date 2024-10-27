import requests
from bs4 import BeautifulSoup
import smtplib
import os
amazon_product_url = "https://www.amazon.ca/gp/product/B0BNF43SWG/ref=ox_sc_act_image_1?smid=A1L7F5DL4H71TK&psc=1"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
accept_language = "en-US,en;q=0.9"
headers = {
    "User-Agent": user_agent,
    "Accept-Language": accept_language
}
response = requests.get(url=amazon_product_url, headers=headers)
webpage_html = response.text
# print(webpage_html)
soup = BeautifulSoup(webpage_html, "html.parser")
price_tag = soup.find(class_="a-offscreen")
price_currency = price_tag.getText()
price_float = price_currency.split("$")[1]
# print(price_float)

title_tag = soup.find(id="productTitle")
title = title_tag.get_text().strip()
#print(title)

my_email = os.environ['EMAIL']
my_password = os.environ['PASSWORD']
target_price = 280
if float(price_float) <= target_price:
    message = f"{title} is now {price_currency}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject: Amazon Price Alert!\n\n{message}\n\n{amazon_product_url}".encode("utf-8")
        )
