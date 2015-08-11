#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Hito http://www.hitoy.org
import socket
import smtplib
import time
import sys
import re
import dkim

hostname=socket.gethostname()
XMailer="PYSMTP-Client-By-Hito 2.1"

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
        self.subject = "" if not args.has_key('subject') else args['subject']
        self.mailfrom = self.sender if not args.has_key('mailfrom') else args['mailfrom']
        self.contenttype = "text/html;charset=utf-8" if not args.has_key('contenttype') else args['contenttype']
        self.dkim = None if not args.has_key('dkim') else args['dkim']

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

        senddate="%s %s"%(time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime()),"+0800")
        messageid="<%s>"%recipient
        mimeversion = "1.0"

        header="From:%s\r\nTo:%s\r\nSubject:%s\r\nMIME-Version:%s\r\nMessage-Id:%s\r\nDate:%s\r\nX-Mailer:%s\r\nContent-Type:%s"%(self.mailfrom,recipient,self.subject,mimeversion,messageid,senddate,XMailer,self.contenttype)
        content="%s\r\n\r\n%s"%(header,body)
        content ==  dkim.rfc822_parse(content)

        if self.dkim:
            domain = re.search(r"[^@]+$",self.mailfrom.strip()).group(0)
            sig = dkim.sign(content,'_dkim',domain,open(self.dkim).read(),include_headers=["From","To","Subject","Date","Message-Id","X-Mailer"],canonicalize=(dkim.Simple, dkim.Relaxed))
            content = sig + content

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
