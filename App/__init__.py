'''
@Author EndlessPeak
@Data 2023/8/8
在本文件中创建flask应用
'''

'''
导入flask框架，本文件将包含以下内容:
1. flask
'''
from flask import Flask 
import secrets
import json
import os
'''
引入需要注册的蓝图变量
'''
from App.views.views_user import blue_user,blue_test
from App.views.views_admin import blue_admin
from App.extensions import init_extensions

def get_db_config():
    '''
    该函数用于获取配置文件的内容
    '''
    with open('App/static/db_config.json','r') as file:
        config = json.load(file)
    return config

def create_app():
    '''
    该函数用于创建flask应用
    
    参数：
    __name__ 用于确定应用位置，以及寻找应用中其他文件的位置，如图像和模板

    返回值为创建的flask应用
    '''

    # 定义应用
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(blueprint=blue_user)
    app.register_blueprint(blueprint=blue_admin,url_prefix="/admin")
    app.register_blueprint(blueprint=blue_test,url_prefix="/test")

    '''
    配置项目的真正项目根目录，原因见下面的说明
    '''
    app.config['PROJECT_ROOT'] = os.path.dirname(app.root_path)

    # 设置上传、推理和裁剪文件的保存位置
    '''
    注意：
    执行 app.py 时，所有的路径都是相对项目根目录的
    但是对于 flask app 项目来说，所有的路径都是相对 App 目录的
    因此下面配置的路径只能用于一般的业务代码
    在遇到 send_from_directory 时，需要取 current_app.root_path 的父级目录
    '''
    UPLOAD_IMAGE_FOLDER = './App/sources/upload_image/'
    INFER_IMAGE_FOLDER = './App/sources/infer_image/'
    CROP_IMAGE_FOLDER = './App/sources/crop_image/'
    app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
    app.config['INFER_IMAGE_FOLDER'] = INFER_IMAGE_FOLDER
    app.config['CROP_IMAGE_FOLDER'] = CROP_IMAGE_FOLDER

    # 设置密钥，用长度为16的十六进制随机字符串作为密钥
    app.secret_key = secrets.token_hex(16)

    '''
    配置数据库
    1. 获取数据库配置信息
    2. 根据配置信息初始化数据库连接地址
    3. 配置数据库
    '''
    db_config = get_db_config()
    db_uri = 'mysql+pymysql://{}:{}@{}/{}'.format(
        db_config['user'],
        db_config['password'],
        db_config['host'],
        db_config['database']
    )
    # print(db_uri)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri          # 配置数据库网址
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # 禁用对象追踪修改
    app.config['SQLALCHEMY_ECHO'] = True                    # 打印调试信息

    # 初始化插件
    init_extensions(app=app)

    # 返回应用
    return app