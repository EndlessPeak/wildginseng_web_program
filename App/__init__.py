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
'''
引入需要注册的蓝图变量
'''
from App.views.views_user import blue_user # blue_test
from App.views.views_admin import blue_admin
from App.extensions import init_extensions

def get_db_config():
    '''
    该函数用于获取配置文件的内容
    '''
    with open('./static/config.json','r') as file:
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
    # app.register_blueprint(blueprint=blue_test)

    # 设置上传、推理和裁剪文件的保存位置
    UPLOAD_IMAGE_FOLDER = './sources/upload_image/'
    INFER_IMAGE_FOLDER = './sources/infer_image/'
    CROP_IMAGE_FOLDER = './sources/crop_image/'
    app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
    app.config['INFER_IMAGE_FOLDER'] = INFER_IMAGE_FOLDER
    app.config['CROP_IMAGE_FOLDER'] = CROP_IMAGE_FOLDER

    # 设置密钥，用长度为16的十六进制随机字符串作为密钥
    app.secret_key = secrets.token_hex(16)

    '''
    配置数据库
    '''
    db_config = get_db_config()
    db_uri = 'mysql+pymysql://{}:{}@{}/{}'.format(
        db_config['user'],
        db_config['password'],
        db_config['host'],
        db_config['database']
    )
    print(db_uri)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri          # 配置数据库网址
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # 禁用对象追踪修改

    # 初始化插件
    init_extensions(app=app)

    # 返回应用
    return app