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

"""
# 数据获取备注
http://hq.sinajs.cn/list=of160119
（注：只需将标黄部分改为所需要的开放式基金代码即可查询该基金的最新单位净值。）

双击后看到了什么？
var hq_str_of160119="南方中证500ETF联接(LOF),1.5548,1.6548,1.5581,-0.21,2016-09-23";

网站返回了一串字符串，其中包含了基金名称、最新单位净值、最新累计单位净值、上一期净值、日增长率、最新净值日期等元素。将字符串抓取下来后，用Excel等工具简单处理，即可获得基金最新的净值，这里从略。

# 数据操作思路

数据获取后，需要对价格进行判断：

time
 - 定时执行脚本，在晚上11点的时候，输出当天的净值（基金更新时间）
 - 判断当前日期，与上一次的买入时间进行比较

price
 - 买入的初步条件就是低于上一次买入价
 - 连续30天未买入，进行邮件提示
 - 连续60天未买入，人工择机买入/输出近60天的净值情况进行判断

 # 具体判断逻辑

 1. 比上一次买入价格相比，跌幅超过2.5%的进行提示；
 2. 连续30天未买入且价格低于上一次买入价的时候进行提示；
 3. 连续60天未买入时进行提示。

 # 邮件提醒

 1. 邮件内容为通用的输出全部信息；
 2. 邮件标题根据触发条件的不同进行了相应的设置。

 # 后续待添加

 1. 进行判断的时候输出近30/60的净值浮动表；
 2. 考虑增加图标渲染功能。

"""
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
    fromaddr = 'seoguess@163.com'
    toaddrs  = '61705345@qq.com'
    msg = MIMEText(content)
    msg['Subject'] = title
    msg['From'] = 'seoguess@163.com'
    msg['To'] = '61705345@qq.com'
    username = 'seoguess@163.com'
    password = 'huangdonghui'

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
    _down = ((_price1-_price2)/_price1) * 100
    #将字符型的日期转化成datetime, 然后进行计算，最后利用datetime.timedelta进行格式化（.days），输出间隔天数，这边返回的天数为整型
    _split = (datetime.strptime(fund_date, '%Y-%m-%d') - datetime.strptime(fund_dict[i][0], '%Y-%m-%d')).days
    content = "%s: 当前价格为 %s，上一次买入价格为 %s，累计跌幅达到 %.2f%%，时间间隔天数为 %s。" % (fund_name, fund_price, _price2, _down, _split)
    content = content.encode('UTF-8')
    # content = "something"
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











# 占位。
