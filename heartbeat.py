#!/usr/bin/python
# -*- coding:utf-8 -*-
# Created Time: Wed Mar 11 00:47:56 2015
# Purpose: Check if remote server is down.
# Mail: hewr2010@gmail.com
__author__ = "Wayne Ho"

import os
import sys
import time
import smtplib
from email.mime.text import MIMEText

import argparse
parser = argparse.ArgumentParser(description="./heartbeat IP")
parser.add_argument("ip", help="ip address of remote server")
parser.add_argument("-t", "--timeout", type=int, default=3,
                    help="ping timeout(s)")
parser.add_argument("-f", "--failure", type=int, default=10,
                    help="maximum failure times")
arg = parser.parse_args()


def ping(server, timeout):
    return os.system("ping -c 1 -t %d %s > /dev/null 2>&1"
                     % (timeout, server)) == 0


def send_alert(subject, content):
    # parameters
    mail_user = "hwr12@mails.tsinghua.edu.cn"
    mail_passwd = ""
    mail_to = "422033281@qq.com"
    mail_cc = "hewr2010@gmail.com"
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

if __name__ == "__main__":
    server = arg.ip
    timeout = arg.timeout
    max_failure = arg.failure
    failure = 0
    while True:
        if ping(server, timeout):
            failure = 0
            print "\r[%s] %s is up" % (time.asctime(), server),
            sys.stdout.flush()
        else:
            failure += 1
            if failure == max_failure:
                send_alert("alert %s" % server, "%s is down!" % server)
                print "\n%s is down!!!!" % (server)
        time.sleep(1)
