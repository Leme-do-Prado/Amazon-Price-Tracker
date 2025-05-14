import smtplib
from bs4 import BeautifulSoup
import requests

MY_EMAIL_ADDRESS = ""
MY_EMAIL_PASSWORD = ""

url = "https://www.amazon.com.br/Pais-filhos-Ivan-Turgu%C3%AAniev/dp/8535932321/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

min_price = 50
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Erro ao acessar a página:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")
price_element = soup.select_one("span.a-price-whole")

if price_element:
    price_str = price_element.get_text(strip=True).replace(".", "").replace(",", "")
    product_price = int(price_str)
    print(f"Preço atual: R${product_price}")

    if product_price <= min_price:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL_ADDRESS, MY_EMAIL_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL_ADDRESS,
                to_addrs=MY_EMAIL_ADDRESS,
                msg=f"Subject:Alerta de Preço Amazon!\n\nO livro está por R${product_price}!\n{url}".encode("utf-8")
            )
else:
    print("Preço não encontrado na página.")
