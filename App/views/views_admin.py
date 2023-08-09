'''
在本文件中写入普通用户的路由和视图函数
1.使用蓝图进行路由注册，取代 app.route
2.建议一个蓝图变量绑定一组目的相同的路由
3.本文件使用 user 作为普通用户的蓝图路由
'''

'''
导入flask框架，本文件将包含以下内容:
1. Blueprint            蓝图
2. request              请求上下文，封装HTTP请求中的内容
3. send_from_directory  从指定目录发送文件响应到客户端
4. current_app          应用上下文，指代当前应用的应用实例
5. render_template      
6. session              请求上下文，用户会话，存储请求间需要记住的值
7. jsonify              用于json数据序列化，将数据对象变成json字符串  
'''
from flask import Blueprint, request, send_from_directory, \
    current_app,render_template , session, jsonify, redirect, url_for

'''
配置蓝图
__name__ 参数指代应用
'''
blue_admin = Blueprint('admin',__name__)