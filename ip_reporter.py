#!/usr/bin/python
# -*- coding:utf-8 -*-
# Created Time: 2015年03月31日 星期二 10时33分30秒
# Purpose: report ip address
# Mail: hewr2010@gmail.com
__author__ = "Wayne Ho"

import os
import sys
import time
import smtplib
from email.mime.text import MIMEText

fin = open("./account.conf")
mail_user = fin.readline()[:-1]
mail_passwd = fin.readline()[:-1]
mail_to = fin.readline()[:-1]
mail_cc = fin.readline()[:-1]
server_addr = fin.readline()[:-1]


def send_alert(subject, content):
    # configuration
    msg = MIMEText(content)
    msg['From'] = mail_user
    msg['Subject'] = subject
    msg['To'] = mail_to
    try:
        s = smtplib.SMTP()
        s.connect("mails.tsinghua.edu.cn")
        s.login(mail_user, mail_passwd)
        s.sendmail(mail_user, [mail_to, mail_cc], msg.as_string())
        s.close()
    except Exception, e:
        print e


def send_ip(ip):
    with open("ip.txt", "w") as fout:
        print >> fout, ip
    os.system("scp ip.txt hewr1993@[%s]:~/" % server_addr)

if __name__ == "__main__":
    last_ip = ""
    while True:
        for line in os.popen("ifconfig | grep 'inet addr'"):
            if line.find("Bcast") != -1:
                line = line[line.find(":") + 1:]
                line = line[:line.find(" ")]
                if line != last_ip:
                    last_ip = line
                    print ""
                    send_alert("ip address has changed", last_ip)
                    send_ip(last_ip)
                print "\r[%s] ip address %s" % (time.asctime(), line),
                sys.stdout.flush()
        time.sleep(1)
