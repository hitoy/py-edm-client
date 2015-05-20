#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Hito http://www.hitoy.org

import socket
import smtplib
import time
import sys

hostname=socket.gethostname()
XMailer="EDM-Client-By-Hito(http://www.hitoy.org/) 2.0"
Retry = 3

class SMTPServerError(BaseException):

    def __init__(self,*args):
        self.value=args[0]

    def __str__(self):
        return repr(self.value)



class SMTPServer():
    def __init__(self,host,port=25,timeout=10,debug=False):
        self.host=host
        self.port=25
        self.timeout=timeout
        try:
            self.server=smtplib.SMTP(host,port,timeout=timeout)
        except Exception,e:
            raise SMTPServerError(e)
        if debug:self.server.set_debuglevel(1)

    def login(self,username,password,ssl=False):
        try:
            if ssl: self.server.starttls()
            self.server.login(username,password)
        except Exception,e:
            raise SMTPServerError(e)

    def add_sender(self,sender):
        self.sender=sender

    def add_header(self,**args):
        self.Subject = "" if not args.has_key('subject') else args['subject']
        self.MailFrom = self.sender if not args.has_key('mailfrom') else args['mailfrom']
        self.ContentType = "text/html;charset=utf-8" if not args.has_key('contenttype') else args['contenttype']

    def send(self, *args):
        """
        Must Be Two Parameters recipient and email body
        """
        if not args:
            raise SMTPServerError("Fatal error: Email Content must have the recipient and body") 
        if len(args) == 1:
            raise SMTPServerError("Fatal error: Email Content must have the body") 

        """
        try:
            self.server.connect(self.host,self.port)
        except Exception,e:
            raise SMTPServerError(e)
        """

        recipient=args[0]
        body=args[1]
        senddate="%s %s"%(time.ctime(),"+0800")

        header="Subject:%s\r\nFrom:%s\r\nTo:%s\r\nContent-Type:%s\r\nDate:%s\r\nX-Mailer:%s"%(self.Subject,self.MailFrom,recipient,self.ContentType,senddate,XMailer)
        content="%s\r\n\r\n%s"%(header,body)
       
        global Retry
        while True:
            try:
                self.server.sendmail(self.sender,recipient,content)
                return True
                break
            except smtplib.SMTPServerDisconnected:
                if Retry == 0:
                    raise SMTPServerError("Lost the Connection withe the Server")
                    return False
                    break
                else:
                    try:
                        self.server.connect()
                        Retry = Retry - 1
                    except:
                        pass
            except Exception,e:
                if Retry == 0:
                    raise SMTPServerError(e)
                    return False
                    break
                else:
                    Retry = Retry - 1
    

        def __del__(self):
            self.server.quite()

"""
m1=SMTPServer("email-smtp.us-west-2.amazonaws.com",25,debug=True)
m1.login("fjdsofdjsfoflaf","fjdosfjdsofafdsgdsfsdaf",True)
m1.add_sender('sales@wayata.com')
m1.add_header(subject="TEST　MAIL",mailfrom="sales@wayata.com")

try:
    m1.send("vip@hitoy.org","haha")
except SMTPServerError,e:
    print e
#m2=SMTPServer("198.11.183.135")
m2.add_sender('sales@wayata.com')
m2.add_header(subject="TEST　MAIL",mailfrom="sales@wayata.com")

try:
    m2.send("cleverlyboy@sina.com","hahahahahahaah")
except SMTPServerError,e:
    print e
"""
