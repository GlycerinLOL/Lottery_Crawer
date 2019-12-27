import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import sys,io,os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

res = 'https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
id1='Lotto649Control_history_dlQuery_SNo%s'
id2='_0'
r = requests.get(res) #get網頁資料
index = BeautifulSoup(r.text,'html.parser') #將網頁資料轉成html.parser
#--------------------------------------------------------------------------------
lottery_time = index.find('span',{'id':'Lotto649Control_history_dlQuery_L649_DDate_0'})
time = lottery_time.text #儲存開獎時間
lottery_total = index.find('span',{'id':'Lotto649Control_history_dlQuery_Total_0'})
total = lottery_total.text #儲存當期獎金總額
#--------------------------------------------------------------------------------
num_list = []
for i in range(1,7):
    lottery_num = i
    lottery_id = id1%(lottery_num)+id2
    normal = index.find('span',{'id':lottery_id})
    num = normal.text
    num_list.append(num) #儲存普通中獎號資料
#--------------------------------------------------------------------------------    
super_ = index.find('span',{'id':'SuperLotto638Control_history1_dlQuery_SNo7_0'})
super_lottery = super_.text #特別獎號碼
#--------------------------------------------------------------------------------
data = {}
data['latest_number'] = []
data['latest_number'].append({
    '開獎日期': time,
    '獎金總額': total,
    '普通獎': num_list,
    '特別獎': super_lottery,
})
print(data)
output_json = json.dumps(data, ensure_ascii=False)
file_name = 'lottery_number.json'
if os.path.isfile(file_name):
    print('exist')
    fp = open(file_name,'r')
    json_original = fp.read()
    fp.close

    output = json_original.strip()[:-1]+','
    output += output_json[1:]
    fp = open(file_name,'w')
    fp.write(output)
    fp.close
else:
    fp = open(file_name,'w')
    fp.write(output_json)
    fp.close