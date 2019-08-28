# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import abort
import hashlib
import xmltodict
import time
import re
import requests

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

        token = "test123" #token验证

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

    	event = xml_dict.get("Event")

    	if event == "subscribe":
    		resp_dict = {
    			"xml":{
    				"ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "关注成功！\n查询小助手当前功能有：\n1.天气查询（天气 地名）\n2.快递查询（快递查询 单号）\n3.公交查询（x路）\n\n当前开发试用阶段"
                }
            }

    	if msg_type == "text":
    		# 表示发送的是文本消息
    		# 构造返回值，经由微信服务器恢复给用户的消息内容
            content = xml_dict.get("Content")
            if "天气" in content:
                url = "https://www.tianqiapi.com/api/?version=v6&city="
                b = content.strip("天气")
                r='[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+' # 正则删除标点符号
                c=re.sub(r,'',b)
                post = c.strip(" ")
                appid = "&appid=1001&appsecret=5566" # 现在要appid或appsecret 否则报错
                url_now = url + post + appid
                rs_we = requests.get(url_now).json()
                weather_city = rs_we["city"]
                if weather_city == post:
                    weather_uptime = rs_we["date"] + " " + rs_we["week"] + " " + rs_we["update_time"] # 更新时间
                    weather_wea = rs_we["wea"] # 天气情况
                    weather_tem = rs_we["tem"] + "℃" # 当前温度
                    weather_temnow = rs_we["tem2"] + "/" + rs_we["tem1"] + "℃" # 早晚温差
                    weather_win = rs_we["win"] # 风向
                    weather_win_speed = rs_we["win_speed"] # 风速等级
                    weather_win_meter = rs_we["win_meter"] # 风速
                    weather_humidity = rs_we["humidity"] # 湿度
                    weather_visibility = rs_we["visibility"] # 能见度
                    weather_pressure = rs_we["pressure"] + "hPa" # 气压
                    weather_air = rs_we["air"] # 空气质量
                    weather_air_pm25 = rs_we["air_pm25"] # PM2.5
                    weather_air_level = rs_we["air_level"] # 空气质量等级
                    weather_info = weather_city + "-今日天气预报（实时）：" + "\r\n当前温度：" + weather_tem + "\r\n早晚温差：" + weather_temnow + "\r\n天气情况：" + weather_wea + "\r\n湿度：" + weather_humidity + "\r\n空气质量：" + weather_air + "\r\nPM2.5：" + weather_air_pm25 + "\r\n空气质量等级：" + weather_air_level + "\r\n气压：" + weather_pressure + "\r\n风向：" + weather_win + "\r\n风速：" + weather_win_meter + "\r\n风速等级：" + weather_win_speed + "\r\n能见度：" + weather_visibility + "\r\n更新时间：" + weather_uptime
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": weather_info
                        }
                    }
                else:
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": "当前地区无法查询天气"
                        }
                    }
            elif "快递查询" in content:
                url = "https://m.kuaidi100.com/apicenter/kdquerytools.do?method=autoComNum&text="
                b = content.strip("快递查询")
                r='[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+' # 正则删除标点符号
                c=re.sub(r,'',b)
                post = c.strip(" ")
                if post == "":
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": "注意快递查询格式（快递查询 单号）"
                        }
                    }

                else:
                    url_now = url + post
                    rs_we = requests.get(url_now).json()
                    kd_message = rs_we["auto"]
                    if  len(kd_message):
                        url2 = "https://m.kuaidi100.com/result.jsp?nu="
                        url_auto = url2 + post
                        resp_dict = {
                            "xml":{
                                "ToUserName": xml_dict.get("FromUserName"),
                                "FromUserName": xml_dict.get("ToUserName"),
                                "CreateTime": int(time.time()),
                                "MsgType": "text",
                                "Content": "快递单号" + post + "结果： \n<a href=\"" + url_auto +"\">点击查看物流</a>"
                            }
                        }
                    else:
                        resp_dict = {
                            "xml":{
                                "ToUserName": xml_dict.get("FromUserName"),
                                "FromUserName": xml_dict.get("ToUserName"),
                                "CreateTime": int(time.time()),
                                "MsgType": "text",
                                "Content": "无法识别当前单号"
                            }
                        }
            elif "路" in content:
                url = "http://mp.zsgcgj.com:10251/buswechat/weixin/initLinePage.action?lineName="
                b = content.strip("路")
                bus = b.strip(" ")
                url_bus = url + bus
                if bus.isdigit(): # 判断是否数字
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": bus + "路公交查询结果： \n<a href=\"" + url_bus +"\">点击查看</a>"
                        }
                    }
                else:
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": "公交查询格式不正确"
                        }
                    }

            elif content == "查询" or content == "功能" or content == "菜单" or content == "帮助":
                resp_dict = {
                    "xml":{
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": "查询小助手当前功能有：\n1.天气查询（天气 地名）\n2.快递查询（快递查询 单号）\n3.公交查询（x路）\n\n当前开发试用阶段"
                    }
                }

    	# 将字典转换成为xml字符串
    	resp_xml_str = xmltodict.unparse(resp_dict)
    	# 返回消息数据给微信服务器
    	return resp_xml_str

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)