# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import abort
import hashlib
import xmltodict
import time

token = "test123"

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/wechat", methods=["GET","POST"])
def weixin():
    if request.method == "GET":     # 判断请求方式是GET请求
        my_signature = request.args.get('signature')     # 获取携带的signature参数
        my_timestamp = request.args.get('timestamp')     # 获取携带的timestamp参数
        my_nonce = request.args.get('nonce')        # 获取携带的nonce参数
        my_echostr = request.args.get('echostr')         # 获取携带的echostr参数

        if not all([my_signature, my_timestamp, my_nonce, my_echostr]):
        	abort(400)
        #token = 'test123'     # 一定要跟刚刚填写的token一致

        # 进行字典排序
        data = [token,my_timestamp ,my_nonce ]
        data.sort()

        # 拼接成字符串
        temp = ''.join(data)

        # 进行sha1加密
        mysignature = hashlib.sha1()
        mysignature.update(temp.encode('utf-8'))
        res = mysignature.hexdigest()
        # 加密后的字符串可与signature对比，标识该请求来源于微信
        if my_signature == res:
            return my_echostr
        else:
        	abort(403)
    elif request.method == "POST":     # 判断请求方式是POST请求
    	xml_str = request.data
    	if not xml_str:
    		abort(400)

    	# 对xml字符串进行解析
    	xml_dict = xmltodict.parse(xml_str)
    	xml_dict = xml_dict.get("xml")

    	# 提取消息类型
    	msg_type = xml_dict.get("MsgType")

    	if msg_type == "text":
    		# 表示发送的是文本消息
    		# 构造返回值，经由微信服务器恢复给用户的消息内容
    		resp_dict = {
    			"xml":{
    				"ToUserName": xml_dict.get("FromUserName"),
    				"FromUserName": xml_dict.get("ToUserName"),
    				"CreateTime": int(time.time()),
    				"MsgType": "text",
    				"Content": xml_dict.get("Content")
    			}
    		}
    	elif msg_type == "image":
            resp_dict = {
                "xml":{
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "test pic"
                }
            }

    	# 将字典转换成为xml字符串
    	resp_xml_str = xmltodict.unparse(resp_dict)
    	# 返回消息数据给微信服务器
    	return resp_xml_str

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
