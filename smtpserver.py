#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Hito http://www.hitoy.org

import socket
import smtplib
import time
import sys

hostname=socket.gethostname()
XMailer="EDM-Client-By-Hito 2.0"

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
        self.server=smtplib.SMTP()
        if debug:self.server.set_debuglevel(1)
        self.ssl=False

    def auth(self,username,password,ssl=False):
        self.username=username
        self.password=password
        self.ssl=ssl

    def connect(self):
        try:
            self.server.connect(self.host,self.port)
            if self.ssl:
                self.server.starttls()
                self.server.login(self.username,self.password)
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
       
        Retry = 3
        while True:
            try:
                self.server.sendmail(self.sender,recipient,content)
                return True
                break
            except smtplib.SMTPServerDisconnected:
                if Retry == 0:
                    raise SMTPServerError("Lost the Connection with the Server")
                    return False
                    break
                else:
                    try:
                        self.connect()
                        Retry = Retry - 1
                    except:
                        Retry = Retry - 1
            except Exception,e:
                if Retry == 0:
                    raise SMTPServerError(e)
                    return False
                    break
                else:
                    Retry = Retry - 1
    

        def __del__(self):
            self.server.quite()

if __name__ == "__main__":
    sys.exit(-1)
