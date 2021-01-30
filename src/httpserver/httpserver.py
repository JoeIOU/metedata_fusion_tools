# httpserver.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==============================================================================
# @Time    : 2020/3/5 14:06
# @Author  : lin.jili
# @File    : httpserver.py
# @Site    : 
# @Desc    : 
# ==============================================================================

from flask import Flask
from flask_cors import CORS
import _thread as th

app = Flask(__name__)
app.secret_key = "iJJafwefHHweLS@hKH!$WHdsd*&H9797HIwqdwq@2121r398hsacsa@INpPFTV@kvdsdsddsv7UVVwfwef"
CORS(app, supports_credentials=True)


def getApp():
    return app


def startWebServer():
    app.debug = False
    app.run(port=8888, host="127.0.0.1", threaded=True)  # 8080


def startServer():
    th.start_new_thread(startWebServer, ())


if __name__ == '__main__':
    # Turn off on PRO environment
    # app.debug = False
    # app.run(port=8888, host="0.0.0.0" ,debug=True, threaded=True)

    startWebServer()
