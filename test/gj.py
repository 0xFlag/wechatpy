def z():
	num = input("公交查询 格式（28路）")

	url = "http://mp.zsgcgj.com:10251/buswechat/weixin/initLinePage.action?lineName=" + num

	print (url)

if __name__ == '__main__':
	z()

#https://blog.csdn.net/qq_41912505/article/details/81533386

#https://m.ickd.cn/result.html#no=70124713784638&com=auto


#https://m.kuaidi100.com/apicenter/kdquerytools.do?method=autoComNum&text=70124713784638

#https://m.kuaidi100.com/result.jsp?nu=1231

#http://mp.zsgcgj.com:10251/buswechat/wechat/index.jsp

# http://mp.zsgcgj.com:10251/buswechat/weixin/searchLine/getAutoCompleteLine.action?term=28

# http://mp.zsgcgj.com:10251/buswechat/weixin/initLinePage.action?lineName=28%E8%B7%AF&isUpDown=0

# http://mp.zsgcgj.com:10251/buswechat/weixin/getWaiting.action?lineName=28&isUpDown=1&stationNum=1