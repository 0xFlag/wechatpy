# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import abort
import hashlib
import xmltodict
import time
import requests

token = "test123"
MY_WEATHER_KEY = r"d2ae781d61744d65a2ef2156eef2cb64"
URL_NOW_WEATHER = r"https://free-api.heweather.net/s6/weather/now?location=auto_ip&key="+MY_WEATHER_KEY # 实时天气
URL_FOR_WEATHER = r"https://free-api.heweather.net/s6/weather/forecast?location=auto_ip&key="+MY_WEATHER_KEY  #预测天气

URL_NOW_WEATHER_CID = r"https://free-api.heweather.net/s6/weather/now?location="
URL_FOR_WEATHER_CID = r"https://free-api.heweather.net/s6/weather/forecast?location="
URL_TAIL_CID = r"&key="+MY_WEATHER_KEY

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
            content = xml_dict.get("Content")
                        # 表示发送的是文本消息
            # 构造返回值，经由微信服务器恢复给用户的消息内容
            if content[0:2] == u"天气":
                post = str(content[2:])
                url_now = URL_NOW_WEATHER_CID + post + URL_TAIL_CID
                rs_we = requests.get(url_now).json()

                wea_status = rs_we["HeWeather6"][0]["status"]
                if wea_status == "ok":
                    wea_info_str = rs_we["HeWeather6"][0]["now"]["cond_txt"]
                    weat_info = (wea_info_str + "  " + rs_we["HeWeather6"][0]["now"]["tmp"] + "度  "+rs_we["HeWeather6"][0]["now"]["wind_dir"] + "  " + rs_we["HeWeather6"][0]["now"]["wind_sc"] + "级")
                    url_forecast = URL_FOR_WEATHER_CID + post + URL_TAIL_CID
                    rs_we = requests.get(url_forecast).json()
                    forewea_info_str = rs_we["HeWeather6"][0]["daily_forecast"][1]["cond_txt_d"]
                    foreweat_info = (wea_info_str + "  " + 
                                        rs_we["HeWeather6"][0]["daily_forecast"][1]["tmp_min"] + " ~ " + 
                                        rs_we["HeWeather6"][0]["daily_forecast"][1]["tmp_max"] + "度  " + 
                                        rs_we["HeWeather6"][0]["daily_forecast"][1]["wind_dir"] + " " + 
                                        rs_we["HeWeather6"][0]["daily_forecast"][1]["wind_sc"] + "级")
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": post+"今日天气预报：\r\n"+weat_info+"\r\n明日天气预报：\r\n"+foreweat_info
                        }
                    }
                elif wea_status == "unknown location":
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": "您查询的区域无法显示天气"
                        }
                    }
                else:
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": "网站出问题"
                        }
                    }
            elif content[2:4] == u"天气":
                post = str(content[:2])
                url_now = URL_NOW_WEATHER_CID + post + URL_TAIL_CID
                rs_we = requests.get(url_now).json()

                wea_status = rs_we["HeWeather6"][0]["status"]
                if wea_status == "ok":
                    wea_info_str = rs_we["HeWeather6"][0]["now"]["cond_txt"]
                    weat_info = (wea_info_str + "  " + rs_we["HeWeather6"][0]["now"]["tmp"] + "度  "+rs_we["HeWeather6"][0]["now"]["wind_dir"] + "  " + rs_we["HeWeather6"][0]["now"]["wind_sc"] + "级")
                    url_forecast = URL_FOR_WEATHER_CID + post + URL_TAIL_CID
                    rs_we = requests.get(url_forecast).json()
                    forewea_info_str = rs_we["HeWeather6"][0]["daily_forecast"][1]["cond_txt_d"]
                    foreweat_info = (wea_info_str + "  " + 
                                        rs_we["HeWeather6"][0]["daily_forecast"][1]["tmp_min"] + " ~ " + 
                                        rs_we["HeWeather6"][0]["daily_forecast"][1]["tmp_max"] + "度  " + 
                                        rs_we["HeWeather6"][0]["daily_forecast"][1]["wind_dir"] + " " + 
                                        rs_we["HeWeather6"][0]["daily_forecast"][1]["wind_sc"] + "级")
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": post+"今日天气预报：\r\n"+weat_info+"\r\n明日天气预报：\r\n"+foreweat_info
                        }
                    }
                elif wea_status == "unknown location":
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": "您查询的区域无法显示天气"
                        }
                    }
                else:
                    resp_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": "网站出问题"
                        }
                    }

    resp_xml_str = xmltodict.unparse(resp_dict)
    return resp_xml_str

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)