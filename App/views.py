'''
在本文件中写入路由和视图函数
1.使用蓝图进行路由注册，取代 app.route
2.建议一个蓝图变量绑定一组目的相同的路由
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
# from App.models import *

'''
配置蓝图
__name__ 参数指代应用
'''
blue_root = Blueprint('root',__name__)
blue_user = Blueprint('user',__name__)
blue_infer = Blueprint('infer',__name__)
# 用于测试的蓝图路由，不在app中注册蓝图
blue_test = Blueprint('test',__name__)

'''
登录路由
'''
@blue_root.route('/login')
def user_login():
    return "Login page."

# 检查登录状态
def check_login_status():
    pass
    return True

# 请求前钩子函数，判断用户登录状态
@blue_root.before_request
def check_login_route():
    # print(request.endpoint)
    if request.endpoint != "root.user_login" and not check_login_status():
        # 实际上就是 redirect("/login")
        return redirect(url_for("root.user_login")) 

'''
根路由，以及相关的路由
'''
@blue_root.route('/')
def index():
    return "Hello World."

'''
用于获取上传文件的路由
path    接收路径，可包含斜线
'''
@blue_infer.route('/request_upload_image/<path:filename>')
def serve_upload_image(filename):
    return send_from_directory(current_app.config['UPLOAD_IMAGE_FOLDER'],filename)

@blue_infer.route('/request_infer_image/<path:filename>')
def serve_infer_image(filename):
    return send_from_directory(current_app.config['INFER_IMAGE_FOLDER'],filename)

@blue_infer.route('/request_crop_image/<path:filename>')
def serve_crop_image(filename):
    return send_from_directory(current_app.config['CROP_IMAGE_FOLDER'],filename)

'''
可接收的路由参数
1.string  接收没有斜杠的字符串
2.int     接收整型
3.float   接收浮点型
4.path    接收路径，可包含斜线
5.uuid    只接收uuid字符串
6.any     可以同时指定多种路径，但是只能从有限的选项中选择一个
当接收数据但不知道 int 和 float 接收时，建议使用字符串

请求方式默认支持 GET/HEAD/OPTIONS
能够手动指定的请求包括 GET/POST/HEAD/PUT/DELETE
'''
@blue_test.route('/test/<string:username>')
def get_string(username):
    print(username)
    return 'Hello'

@blue_test.route('/request/', methods=['GET', 'POST'])
def get_request():
    print(request.method)   #请求方式
    print(request.args)     #若为GET请求，则使用args获取参数内容，获取的是类字典对象
    print(request.form)     #若为POST请求，则使用form获取参数内容，获取的也是类字典对象
    print(request.path)     #显示路由
    print(request.cookies)  #cookies
    print(request.url)      #完整url
    print(request.base_url) #路由url
    print(request.host_url) #基本url
    print(request.remote_addr) #客户端IP
    print(request.files)    #文件上传
    print(request.headers)  #请求头
    print(request.user_agent) #用户代理，包含浏览器信息和操作系统信息
    return 'request ok!'