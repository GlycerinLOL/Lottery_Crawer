import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import os

url = 'https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
r = requests.get(url) #get網頁資料
index = BeautifulSoup(r.text,'html.parser') #將網頁資料轉成html.parser
#-------------------函式區-------------------------------------------------------
def crawer(id_):
    a = index.find('span',{'id':id_})
    b = a.text
    return(b)
def Diff(li1, li2): 
    set1,set2 = set(li1),set(li2)
    return(list(set1 & set2))
#--------------------------------------------------------------------------------

term_id = 'Lotto649Control_history_dlQuery_L649_DrawTerm_0' 
term = crawer(term_id) #當期期號
if os.path.exists('termcheck.txt'):
    with open('termcheck.txt','r') as f:
        termcheck = f.read()
    with open('termcheck','w') as f:
        f.write(term)
else:
    with open('termcheck.txt','w') as f:
        f.write(term)
        termcheck = 0
if term != termcheck:
    print('資料已更新')
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
else:
    print('資料未更新')
while True:
    user_term = str(input('請輸入期號: '))
    if len(user_term) != 9:
        print('你的輸入不符合格式')
        continue
    else:
        break
while True:
    user_num = input('請輸入樂透號碼: ')
    if len(user_num) != 12:
        print('你的輸入不符合格式')
        continue
    else:
        break
#--------------------------------------------------------------------------------
user_list = []
flag = 0
for a in range(6):
    user_list.append(user_num[flag]+user_num[flag+1]) #讀取使用者輸入的號碼
    flag += 2
print('你輸入的樂透號碼: %s'%(user_list))
#--------------------------------------------------------------------------------
file_name = 'lottery_number.json'
with open(file_name,'r') as f:
    lottery_data = json.load(f)
data_dict = (lottery_data[user_term])[0]
load_list = data_dict['Normal number'] #從檔案中讀取之前的樂透號碼
same_num = len(Diff(user_list,load_list)) #與普通號比對
#--------------------------------------------------------------------------------
for check in range(6): #檢查特別號
    special = data_dict['Special number']
    special_check = False
    if user_list[check] == special:
        special_check = True
        break
#--------------------------------------------------------------------------------
print('本期期號: %s'%(user_term))
draw_time = data_dict['Latest draw date']
print('本期開獎時間: %s'%(draw_time))

if same_num == 6:
    prize = (data_dict['prize list (first~normal)'])[0]
    print('頭獎 !')
    print('獎金為: %s NTD'%(prize))
elif same_num == 5 and special_check ==True:
    prize = (data_dict['prize list (first~normal)'])[1]
    print('貳獎 !')
    print('獎金為: %s NTD'%(prize))
elif same_num == 5:
    prize = (data_dict['prize list (first~normal)'])[2]
    print('參獎 !')
    print('獎金為: %s NTD'%(prize))   
elif same_num == 4 and special_check ==True:
    prize = (data_dict['prize list (first~normal)'])[3]
    print('肆獎 !')
    print('獎金為: %s NTD'%(prize))
elif same_num == 4:
    prize = (data_dict['prize list (first~normal)'])[4]
    print('伍獎 !')
    print('獎金為: %s NTD'%(prize))
elif same_num == 3 and special_check ==True:
    prize = (data_dict['prize list (first~normal)'])[5]
    print('陸獎 !')
    print('獎金為: %s NTD'%(prize))
elif same_num == 2 and special_check ==True:
    prize = (data_dict['prize list (first~normal)'])[6]
    print('柒獎 !')
    print('獎金為: %s NTD'%(prize))
elif same_num == 3:
    prize = (data_dict['prize list (first~normal)'])[7]
    print('普獎 !')
    print('獎金為: %s NTD'%(prize))
else:
    print('你未中獎!') #中獎判斷式