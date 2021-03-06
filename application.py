# -*- coding:utf-8 -*-
#author: bukun@osgeo.cn

import tornado.web
import os
from urls import urls
from torlite.core.core_cfg import core_modules as modules
# from extend_config import extend_modules
from modules.extends import *

# 定义模板


SETTINGS = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    'debug': True,
    "cookie_secret": "61oETzsdafKasdsdfXQA",
    "login_url": "/user/login",
    'ui_modules':  modules,
}


application = tornado.web.Application(
    handlers=urls,
    **SETTINGS
)

if __name__ == '__main__':
    pass