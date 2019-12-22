import requests
pic = requests.get('https://imgur.dcard.tw/N2k5kV2m.jpg')
catpic = pic.content
pic_out = open('img1.png','wb')
pic_out.write(catpic)
pic_out.close