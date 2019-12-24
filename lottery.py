import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup

res = 'https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
id1='Lotto649Control_history_dlQuery_SNo%s'
id2='_0'
r = requests.get(res) #get網頁資料
index = BeautifulSoup(r.text,'html.parser') #將網頁資料轉成html.parser
print('一般號碼:')
for i in range(1,7):
    lottery_num = i
    lottery_id = id1%(lottery_num)+id2
    normal = index.find('span',{'id':lottery_id})
    num = normal.text
    print('',num) #抓出當期大樂透的六位中獎號
super_ = index.find('span',{'id':'SuperLotto638Control_history1_dlQuery_SNo7_0'})
super_lottery = super_.text
print('特別號:\n',super_lottery) #抓出當期特別號