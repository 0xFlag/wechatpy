import re
import requests
import json

def  a():
	a = input("输入单号：")

	url = "https://m.kuaidi100.com/apicenter/kdquerytools.do?method=autoComNum&text="
	b = a.strip("快递查询")
	r='[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+' # 正则删除标点符号
	c=re.sub(r,'',b)
	post = c.strip(" ")
	url_now = url + post
	rs_we = requests.get(url_now).json()
	kd_message = rs_we["auto"]

	if  len(kd_message):
		print("ok")
	else:
		print("no")

if __name__ == "__main__":
	a()