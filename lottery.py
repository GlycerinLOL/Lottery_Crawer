import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import sys,io,os

res = 'https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
r = requests.get(res) #get網頁資料
index = BeautifulSoup(r.text,'html.parser') #將網頁資料轉成html.parser

def crawer(id_):
    a = index.find('span',{'id':id_})
    b = a.text
    return(b)
#--------------------------------------------------------------------------------
time_id = 'Lotto649Control_history_dlQuery_L649_DDate_0'
lottery_time = crawer(time_id) #儲存開獎時間
total_id = 'Lotto649Control_history_dlQuery_Total_0'
lottery_total = crawer(total_id) #儲存當期獎金總額
#--------------------------------------------------------------------------------
num_list = []
id1='Lotto649Control_history_dlQuery_SNo%s'
id2='_0'
for i in range(1,7):
    lottery_id = id1%(i)+id2
    normal = crawer(lottery_id)
    num_list.append(normal) #儲存普通中獎號資料
#--------------------------------------------------------------------------------
super_id = 'SuperLotto638Control_history1_dlQuery_SNo7_0'    
super_ = crawer(super_id) #特別獎號碼
term_id = 'Lotto649Control_history_dlQuery_L649_DrawTerm_0' 
term = crawer(term_id) #當期期號
#--------------------------------------------------------------------------------
money_list = []
first_id = 'Lotto649Control_history_dlQuery_L649_CategA4_0'
first_value = crawer(first_id)
money_list.append(first_value)
money_id1 = 'Lotto649Control_history_dlQuery_Label%s'
money_id2 = '_0'
for n in range(7,14):
    money_id = money_id1%(n)+money_id2
    money_value = crawer(money_id)   
    money_list.append(money_value) #當期獎金
#--------------------------------------------------------------------------------    
time_now = datetime.now()
time_now = time_now.strftime("%m/%d/%Y, %H:%M:%S")
data = {}
data[term] = []
data[term].append({
    'running time': time_now,
    'Latest draw date': lottery_time,
    'Total money': lottery_total,
    'Normal number': num_list,
    'Special number': super_,
    'prize list (first~normal)': money_list
})
print(data[term]) #大樂透資料存進dict
#--------------------------------------------------------------------------------
output_json = json.dumps(data, ensure_ascii=False)
file_name = 'lottery_number.json'
if os.path.isfile(file_name): #若該json已存在，則印出exist且叫出現有數據並與新數據合併存入
    print('exist')
    fp = open(file_name,'r')
    json_original = fp.read()
    fp.close

    output = json_original.strip()[:-1]+','
    output += output_json[1:]
    fp = open(file_name,'w')
    fp.write(output)
    fp.close
else:                         #若該json不存在，則開一個新json並存入新數據
    fp = open(file_name,'w')
    fp.write(output_json)
    fp.close
#--------------------------------------------------------------------------------
