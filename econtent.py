#!/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
import re
import time

htmltag = re.compile(r"<[^>]+>[^<]+<[^>]+>")

class EcontentParse():

    def __init__(self,content):
        self.content = content
        self.boundary='--=_Part%s_=--'%(time.time())
        if htmltag.search(content)==None:
            self.type='plain'
        else:
            self.type='alternative'

    def get_ContentHeader(self):
        if self.type == 'plain':
            return 'text/plain;charset="utf-8"\r\nContent-Transfer-Encoding: base64'
        elif self.type == 'alternative':
            return 'multipart/alternative;boundary="%s"'%self.boundary


    def get_content(self):
        if self.type=='plain':
            return base64.b64encode(self.content)
        elif self.type=='alternative':
            content = 'This is a multi-part message in MIME format.\r\n'
            notagcontent=re.sub(r"<[^>]+>","",self.content)
            content += "--%s\r\nContent-Type:text/plain;charset=utf-8\r\nContent-Transfer-Encoding: base64\r\n\r\n%s\r\n"%(self.boundary,base64.b64encode(notagcontent))
            content += "--%s\r\nContent-Type:text/html;charset=utf-8\r\nContent-Transfer-Encoding: base64\r\n\r\n%s\r\n--%s--\r\n"%(self.boundary,base64.b64encode(self.content),self.boundary)
            return content
