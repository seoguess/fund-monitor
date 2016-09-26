#!/usr/bin/env python
#coding:utf-8

import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""
http://hq.sinajs.cn/list=of160119
（注：只需将标黄部分改为所需要的开放式基金代码即可查询该基金的最新单位净值。）

双击后看到了什么？
var hq_str_of160119="南方中证500ETF联接(LOF),1.5548,1.6548,1.5581,-0.21,2016-09-23";

网站返回了一串字符串，其中包含了基金名称、最新单位净值、最新累计单位净值、上一期净值、日增长率、最新净值日期等元素。将字符串抓取下来后，用Excel等工具简单处理，即可获得基金最新的净值，这里从略。
"""

def fund_info(num):
    url = "http://hq.sinajs.cn/list=of%s" % str(num)
    try:
        r = requests.get(url)
        cnt = r.text.split(",")
        return (cnt[0][21:],cnt[1],cnt[-1][:10])
    except:
        return None
    finally:
        r.close()

fund_name,fund_price,fund_date = fund_info(160119)
print fund_name,fund_price,fund_date

"""
数据获取后，需要对价格进行判断：

time
 - 定时执行脚本，在晚上11点的时候，输出当天的净值（基金更新时间）
 - 判断当前日期，与上一次的买入时间进行比较

price
 - 买入的初步条件就是低于上一次买入价 >> 应对已经有浮盈/浮亏的基金（下跌）
 - 连续30天未买入，进行邮件提示 >> 应对亏损的基金（上升）
 - 连续60天未买入，人工择机买入/输出近60天的净值情况进行判断

"""








# 占位。
