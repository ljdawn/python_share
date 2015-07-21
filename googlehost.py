#!/usr/bin/env python
#-*- coding: utf-8 -*-
#谷歌host修改脚本
#author pop<hipop#126.com>
#date 01/05/015
#
#【使用说明】
#请确保在当“前用户对host可写”前提下使用；
#AT一下，每天运行一次更健康；
#本品禁止食用、拆解或投入火中；
#小学生请在监护人陪同下一起使用；
#孕妇慎用。
import sys,os
import urllib,urllib2,re
if __name__ == '__main__':
    print u'谷歌host修改脚本\nauthor pop<hipop#126.com>\n01/05/015\r数据：http://www.360kb.com/kb/2_122.html'

    #load host from 360kb
    htmlH      = urllib2.urlopen('http://www.360kb.com/kb/2_122.html')
    html       = htmlH.read()
    reg        = r'#base services.*#google hosts 2015 end'
    hostHtmlRe = re.search(reg, html, re.S)
    hostHtml   = hostHtmlRe.group()
    hostHtml   = hostHtml.replace('&nbsp;',' ')
    hostHtml   = hostHtml.replace('<span>', '')
    hostHtml   = hostHtml.replace('</span>', '')
    hostStr    = hostHtml.replace('<br />','')

    #write host file
    f          = open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'r+')
    hostOld    = f.read()
    reg        = re.compile(r'\r\n#google=.*#google hosts 2015 end', re.S)
    hostNew    = re.sub(reg, '', hostOld)
    hostNew    = hostNew + '\r\n#google===========================\r\n' + hostStr
    #安全起见，不修改account相关
    reg        = re.compile(r'account', re.S)
    hostNew    = re.sub(reg, 'OOXXaccount', hostNew)
    print hostNew
    f.seek(0)
    f.write(hostNew)
    f.close()
    print 'ok'
