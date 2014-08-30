# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import urllib2 
import os
import sys   
from threading import Timer 
from bs4 import BeautifulSoup
import re
import smtplib
import base64


reload(sys)  
sys.setdefaultencoding('utf-8')  
f = open("urls.txt", "w+")
rawurls = f.readlines()  # 分行读取文件中的链接并存入列表（链接后有换行符）
urls = []
for url in rawurls:
    url = url[::-1]
    url = url[1:]
    url = url[::-1]
    urls.append(url)  # 剪切换行符并把 url 存入 urls 列表


def sendemail(msg):
    """
    发送邮件函数
    :param msg: 邮件标题内容
    """
    username = "monitor@ziqiang.net"
    # 密码
    password = "ziqiang@monitor"
    # smtp会话过程中的mail from地址
    from_addr = "monitor@ziqiang.net"
    # smtp会话过程中的rcpt to地址
    # to_addr = "mobile@ziqiang.net"
    to_addr = "963949236@qq.com"
    svr = smtplib.SMTP()
    svr.connect('smtp.gmail.com:25')
    # 设置为调试模式，就是在会话过程中会有输出信息
    # svr.set_debuglevel(1)
    # ehlo命令，docmd方法包括了获取对方服务器返回信息，如果支持安全邮件，返回值里会有starttls提示
    svr.docmd("EHLO server")
    svr.starttls()  # <------ 这行就是新加的支持安全邮件的代码！
    # 发送正文数据
    svr.login(username, password)
    svr.sendmail(from_addr, to_addr, 'Subject:'+msg)
    print "发送成功"
    # 发送结束，退出
    svr.quit()


def getannonce(name, url_path, comth, comstr, headurl):
    """
    获取公告
    :param name: 网站名称
    :param url_path: 公告所在网址
    :param comth: 需要匹配的属性名称
    :param comstr: 需要匹配的属性值
    :param headurl: URL 前缀
    :return:
    """
    try:
        soup = BeautifulSoup(urllib2.urlopen(url_path, timeout=4))  # 装汤
    except urllib2.HTTPError:
        pass
    else:
        a = soup.find_all("a", attrs={comth: re.compile(comstr)})  # 匹配链接
        for i in a:
            url = i["href"]  # 获取链接
            if url in urls:  # 判断链接是否在列表中
                pass
            else:
                urls.append(url)  # 添加链接到列表中（好像没有用0.0）
                # print url
                f.write(url)  # 添加链接到文件中
                f.write("\n")  # 加换行符分行
                url_ = headurl+url
                if i.strong:  # 有些公告是加粗字体
                    mailstr = "【"+name+"】有新公告！>>>>"+i.strong.string+"\n\n"+url_  # mailstr 中的两个换行符使 url_ 变成正文部分
                    sendemail(mailstr)
                else:
                    mailstr = "【"+name+"】有新公告！>>>>"+i.string+"\n\n"+url_
                    sendemail(mailstr)


def getall():
    """
    获取所有公告信息
    """
    # 官网主页
    getannonce("武大官网", "http://www.whu.edu.cn/tzgg.htm", "href", "info", "http://www.whu.edu.cn/")
    # 电影消息
    getannonce("电影消息", "http://vhost.whu.edu.cn/gh/xywh.php?Class_Type=0&Class_ID=42", "href", "xywh_Cons.php", "http://vhost.whu.edu.cn/gh/")
    # 教务部
    getannonce("教务部", "http://jwb.whu.edu.cn/infocenter.aspx", "href", "Archives", "http://jwb.whu.edu.cn/")
    # 保卫部
    getannonce("保卫部", "http://sub.whu.edu.cn/protect/gzdt/", "class", "url", "http://sub.whu.edu.cn/protect/")
    # 考试中心
    getannonce("考试中心", "http://exam.whu.edu.cn/News/zhks/", "href", "^/News/k", "http://exam.whu.edu.cn")
    # 一站式
    getannonce("一站式", "http://yzs.whu.edu.cn/article/?s=%E4%BF%A1%E6%81%AF%E5%8F%91%E5%B8%83", "href", "yzs.whu.edu.cn/article", "")
    # 学工部
    getannonce("学工部", "http://xgb.whu.edu.cn/list.asp?id=45", "href", "Article.asp", "http://xgb.whu.edu.cn/")
    # 校医院
    getannonce("校医院", "http://hospital.whu.edu.cn/tiltelist.aspx?Newstype=1", "href", "content.aspx", "http://hospital.whu.edu.cn/")
    # 武装部 有两个页面
    getannonce("武装部", "http://rwb.whu.edu.cn/list.asp?id=49", "href", "Article.asp", "http://rwb.whu.edu.cn/")
    getannonce("武装部", "http://rwb.whu.edu.cn/list.asp?id=45", "href", "Article.asp", "http://rwb.whu.edu.cn/")
    # 网络中心
    getannonce("网络中心", "http://nic.whu.edu.cn/", "href", "m=announce", "")
    # 财务部
    getannonce("财务部", "http://finance.whu.edu.cn/finance/wenjiantongzhi/wjtz.htm", "href", "WJTZ", "http://finance.whu.edu.cn/finance/wenjiantongzhi/")
    # 国交中心
    getannonce("国交中心", "http://oir.whu.edu.cn/list/?33_1.html", "href", "content/", "http://oir.whu.edu.cn/")
    # 就业指导中心 列表中包括下一页，尾页链接（index)
    getannonce("就业指导中心", "http://www.xsjy.whu.edu.cn/zxtg//", "href", "zxtg/", "http://www.xsjy.whu.edu.cn/")
    # 实验部 中文乱码，在函数中未添加转码的部分（fromEncoding="gb18030"）
    getannonce("实验部", "http://lab.whu.edu.cn/tzgg/", "href", "tzgg/", "http://lab.whu.edu.cn/")
    # 后勤部
    getannonce("后勤部", "http://hqbzb.whu.edu.cn/list.aspx?id=28", "href", "ShowArticle.aspx", "http://hqbzb.whu.edu.cn/")

print getall()
#循环部分
try:
    Timer(300000, getall()).start()
finally:
    Timer(300000, getall()).start()
