#!/usr/bin/env python
#coding:utf-8

import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#导入时间模块
from datetime import datetime
import time

#导入邮箱模块
import smtplib
from email.mime.text import MIMEText

#导入BeautifulSoup模块
from bs4 import BeautifulSoup
import re

#设置基金标的与上一次买入日期与单价
fund_dict = {160119:["2016-09-12", 1.5359], 320011: ["2016-09-12", 2.46] , 460005: ["2016-09-12", 2.5559], 470009: ["2016-09-12", 2.787]}

#数据获取函数
def fund_info(num):
    url = "http://hq.sinajs.cn/list=of%s" % str(num)
    try:
        r = requests.get(url)
        cnt = r.text.split(",")
        #返回三个字段，基金名称、基金价格以及获取到数据对应的日期
        return (cnt[0][21:],cnt[1],cnt[-1][:10])
    except:
        return None
    finally:
        r.close()

#设置邮件提醒的内容
def email_remind(title,content):
    fromaddr = 'sendmail'
    toaddrs  = 'getmail'
    msg = MIMEText(content)
    msg['Subject'] = title
    msg['From'] = 'sendmail'
    msg['To'] = 'getmail'
    username = 'sendmail'
    password = 'password'

    server = smtplib.SMTP('smtp.163.com')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

for i in fund_dict.keys():
    #迭代并赋值
    fund_name,fund_price,fund_date = fund_info(i)
    #将基金价格转化成float
    _price1 = float(fund_price)
    _price2 = fund_dict[i][1]
    #换算成百分比 * 100
    _down = ((_price2-_price1)/_price1) * 100
    #将字符型的日期转化成datetime, 然后进行计算，最后利用datetime.timedelta进行格式化（.days），输出间隔天数，这边返回的天数为整型
    _split = (datetime.strptime(fund_date, '%Y-%m-%d') - datetime.strptime(fund_dict[i][0], '%Y-%m-%d')).days
    content = "%s: 当前价格为 %s (%s)，上一次买入价格为 %s，累计跌幅达到 %.2f%%，时间间隔天数为 %s。" % (fund_name, fund_price, fund_date, _price2, _down, _split)
    # 将content内容encode成UTF-8格式
    content = content.encode('UTF-8')
    #开始进行逻辑判断，主要是3个条件：
    if _down > 2.5:
        title = "%s 跌幅达到 %.2f%%" % (fund_name, _down)
        email_remind(title,content)

    elif _price1 < _price2 and 30 <= _split < 60:
        title = "%s 超过 %s 天没有买入" % (fund_name,_split)
        email_remind(title,content)

    elif _split >= 60:
        title = "%s 已经有 %s 天没有买入" % (fund_name,_split)
        email_remind(title,content)

    # 格式化字符输出小数点位后面两个字符，重复两个%用于输出一个%
    print content

# 可选 - 输出最近500天的净值波动情况表
num1 = 460005

#数据获取函数
def fund_info2(num):
    url = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=%s&page=1&per=500" % str(num)
    try:
        r = requests.get(url)
        return r.text
    except:
        return None
    finally:
        r.close()

html = fund_info2(num1)
soup = BeautifulSoup(html,'html.parser')
result = soup.find_all("tr")[1:]
# print result

# 新建两个list用来放置时间与价格字段，传递到echarts中
date_list = []
price_list = []
for x in result:
    _date = (x.find_all("td")[0].string).encode('UTF-8')
    _price = (x.find_all("td")[1].string).encode('UTF-8')
    date_list.append(_date)
    price_list.append(_price)

# 将demo1.html作为模板，然后进行字符串格式化输出
with open("demo1.html", "r") as f1:
    _cnt = f1.read()
    cnt = _cnt % (fund_info(num1)[0] ,sorted(date_list), price_list)

with open("demo.html", "w") as f2:
    f2.write(cnt)




#
