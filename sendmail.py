#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Hito http://www.hitoy.org/
import sys
import os
import time
import random
import re
from smtpserver import *
from econtent import EcontentParse

arguments = sys.argv

if len(arguments) == 1:
    sys.stdout.write("Need At least 3 Parameters, 0 gives.\r\n-h for help\n")
    sys.exit(-1)

if "-h" in arguments:
    sys.stdout.write("\tThis is The EDM Client Powered By Hito,Please allow the fllow rules to send a email or a emai list:\n")
    sys.stdout.write("""
    -ef (emailfile)assignation the file store the email you want to send mail to him/her
    -e  (email)assignation the email address you want to send mail to him/her
    -cf (contentfile)assignation the file store the content 
    -c (content) assignation the content you want to send to him/her
    -i set the transmission interval of two messages default 20
    -m set the send mode (rand, turn, select),defalut is rand
    -d run this program as a deamon(Linux)
    
    -subject add the subject of a email.
    -mailfrom add the sender email address.
    -attachment add a attachment (Max 10MB).
    -dkim add a dkim sign of this email.
    """)
    sys.exit(0)

if "-ef" in arguments and "-e" in arguments:
    sys.stdout.write("-ef conflict with -e \n")
    sys.stdout.flush()
    sys.exit(-1)
elif "-ef" in arguments:
    index = arguments.index("-ef")+1
    try:
        emaillist = open(arguments[index],"r")
    except Exception,e:
        sys.stdout.write("%s\n"%e)
        sys.exit(-1)
elif "-e" in arguments:
    index = arguments.index("-e")+1
    emaillist = re.split("[\s,:]+",arguments[index])
elif not("-ef" in arguments) and not("-e" in arguments):
    sys.stdout.write("Must assignation a email address\n")
    sys.stdout.flush()
    sys.exit(-1)


if "-cf" in arguments and "-c" in arguments:
    sys.stdout.write("-cf conflict with -c \n")
    sys.stdout.flush()
    sys.exit(-1)
elif "-cf" in arguments:
    index = arguments.index("-cf")+1
    try:
        content=open(arguments[index],"rb").read()
    except Exception,e:
        sys.stdout.write("%s\n"%e)
        sys.exit(-1)
elif "-c" in arguments:
    index = arguments.index("-c")+1
    content = arguments[index]
elif not("-cf" in arguments) and not("-c" in arguments):
    sys.stdout.write("Must assignation email content\n")
    sys.stdout.flush()
    sys.exit(-1)

if "-i" in arguments:
    index = arguments.index("-i")+1
    try:
        interval=arguments[index]
    except:
        interval=20
else:
    interval = 20

if "-m" in arguments:
    index=arguments.index("-m")+1
    try:
        sendmode = arguments[index]
    except:
        sendmode = "rand"
else:
    sendmod = "rand"

if "-subject" in arguments:
    index=arguments.index("-subject")+1
    try:
        subject = arguments[index]
    except:
        sys.stdout.write("Error: Must Input A Subject of a email")
        sys.exit(-1)
else:
    sys.stdout.write("Error: Must Input A Subject of a email with -subject")
    sys.exit(-1)

if "-mailfrom" in arguments:
    index=arguments.index("-mailfrom")+1
    try:
        mailfrom = arguments[index]
    except:
        sys.stdout.write("Error: Must Input Sender email address")
        sys.exit(-1)
else:
    sys.stdout.write("Error: Must Input Sender email address")
    sys.exit(-1)

if "-dkim" in arguments:
    index=arguments.index("-dkim")+1
    if os.path.isfile(arguments[index]):
        cert = arguments[index]
else:
        cert = None


if "-attachment" in arguments:
    index=arguments.index("-attachment")+1
    if not (os.path.isfile(arguments[index])):
        sys.stdout.write("Error: attachment not found!\n")
    elif os.path.getsize(arguments[index]) > 10*1024*1024:
        sys.stdout.write("Error: attachment too large!\rn")
    else:
        attach = arguments[index]
else:
    attach = None

if "-d" in arguments:
    try:
        pid=os.fork()
    except:
        sys.stdout.write("Your System not support run as a deamon.\n")
        sys.exit(-1)

    if pid:
        sys.exit(0)
    logfile=open("./sendmail.log","a+")
    fd=open("/dev/null","a+")
    os.dup2(fd.fileno(),0)
    os.dup2(fd.fileno(),2)
    os.dup2(logfile.fileno(),1)
    os.setsid()
    os.chdir("/")
    os.umask(0)




try:
    #Connect and login to smtp server
    m1 = SMTPServer("1.1.1.1")
    m2 = SMTPServer("2.2.2.2")
    m2.auth("uername","password",True)
    m1.connect()
    m2.connect()
except SMTPServerError,e:
    sys.stdout.write("%s\n"%e)
    sys.stdout.flush()
    sys.exit(-1)



econtent=EcontentParse(content,attach)
contenttype=econtent.get_ContentHeader()
content=econtent.get_content()



m1.add_sender(mailfrom)
m2.add_sender(mailfrom)
m1.add_header(subject=subject,mailfrom=mailfrom,contenttype=contenttype,dkim=cert)
m2.add_header(subject=subject,mailfrom=mailfrom,contenttype=contentype,dkim=cert)

server = set()
server.add(m1)
server.add(m2)

for i in emaillist:
    email = i.strip()
    smtpserver=server.pop()
    server.add(smtpserver)
    try:
        result = smtpserver.send(email,content)
        sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),email,"Send Success!"))
    except SMTPServerError,e:
        sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),email,e))
    except:
        pass

    sys.stdout.flush()
    interval=int(interval)
    time.sleep(interval)
