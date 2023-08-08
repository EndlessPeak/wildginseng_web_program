'''
在本文件中写入路由和视图函数
1.使用蓝图进行路由注册，取代 app.route
2.建议一个蓝图变量绑定一组目的相同的路由
'''

from flask import Blueprint
from App.models import *

'''
配置蓝图
__name__ 参数指代应用
'''
blue_root = Blueprint('user',__name__)

@blue_root.route('/')
def index():
    return "Hello World."