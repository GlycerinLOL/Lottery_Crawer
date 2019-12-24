import requests
import xlwings as xw
from datetime import datetime
from bs4 import BeautifulSoup

res = 'https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
id1='Lotto649Control_history_dlQuery_SNo%s'
id2='_0'
r = requests.get(res) #get網頁資料
index = BeautifulSoup(r.text,'html.parser') #將網頁資料轉成html.parser
num_list = []
for i in range(1,7):
    lottery_num = i
    lottery_id = id1%(lottery_num)+id2
    normal = index.find('span',{'id':lottery_id})
    num = normal.text
    num_list.append(num)
#print(num_list)    
super_ = index.find('span',{'id':'SuperLotto638Control_history1_dlQuery_SNo7_0'})
super_lottery = super_.text
r_index = 'A'
workbook = xw.Book('lottery.xlsx')
sheet = workbook.sheets['工作表1']
sheet.range('A1:F1').value = num_list
type(sheet.range('A1:F1').current_region.end('down').row)


