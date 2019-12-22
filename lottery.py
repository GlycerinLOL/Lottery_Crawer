import requests
import urllib
from bs4 import BeautifulSoup

res = 'https://www.bloomberg.com/quote/AAPL:US'
r = requests.get(res)
index = BeautifulSoup(r.text,'html.parser')
table = index.find('h1',{'class':'priceText__1853e8a5'})
num = table.text
print(num)