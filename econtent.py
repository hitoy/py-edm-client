#!/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
import re
import time
import os
import math

htmlreg = re.compile(r"<[^>]+>[^<]+<[^>]+>")
pathreg = re.compile(r"[^/]*(\.(\w*))$")

def Long2Email(content):
    if len(content) > 72:
        return "%s\r\n%s"%(content[0:72],Long2Email(content[72:]))
    else:
        return content

class EcontentParse():

    def __init__(self,content,attachment=None):
        self.content = content
        self.boundary = '--=_NextPart%s_=--'%(time.time())
        self.attachment=attachment
        if attachment:
            self.filename=pathreg.search(attachment).group(0)

    def get_ContentHeader(self):
        if self.attachment:
            return 'multipart/mixed;boundary="%s"'%self.boundary
        else:
            return 'multipart/alternative;boundary="%s"'%self.boundary


    def get_txt_content(self,boundary):
            notagcontent=re.sub(r"<[^>]+>","",self.content)
            content = "--%s\r\nContent-Type:text/plain;charset=\"us-ascii\"\r\nContent-Transfer-Encoding: base64\r\n\r\n%s\r\n\r\n"%(boundary,Long2Email(base64.b64encode(notagcontent)))
            content += "--%s\r\nContent-Type:text/html;charset=\"us-ascii\"\r\nContent-Transfer-Encoding: base64\r\n\r\n%s\r\n--%s--\r\n\r\n"%(boundary,Long2Email(base64.b64encode(self.content)),boundary)
            return content

    def get_content(self):
        if self.attachment:
            boundary = '--=_Next_Part%s__=--'%(time.time())
            attachcontent = open(self.attachment,"rb").read()

            content = "--%s\r\nContent-Type: multipart/alternative;\r\nboundary=\"%s\"\r\n\r\n"%(self.boundary,boundary)
            content += self.get_txt_content(boundary)
            content += "\r\n--%s\r\nContent-Type: application/octet-stream;\r\nname=\"%s\"\r\nContent-Disposition: attachment;filename=\"%s\"\r\nContent-Transfer-Encoding: base64\r\n\r\n%s\r\n\r\n--%s--\r\n"%(self.boundary,self.filename,self.filename,Long2Email(base64.b64encode(attachcontent)),self.boundary)
            return "This is a multi-part message in MIME format.\r\n\r\n%s"%(content)
        else:
            return "This is a multi-part message in MIME format.\r\n\r\n%s"%self.get_txt_content(self.boundary)
