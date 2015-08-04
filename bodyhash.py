#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base64,hashlib,sys
body=open(sys.argv[1],"rb").read()
h=hashlib.sha256()
h.update(body)
print base64.b64encode(h.digest())
