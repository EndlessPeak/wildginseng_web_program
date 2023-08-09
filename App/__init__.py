'''
@Author EndlessPeak
@Data 2023/8/8
在本文件中创建flask应用
'''

'''
导入flask框架，本文件将包含以下内容:
Flask
'''
from flask import Flask
import secrets
'''
引入需要注册的蓝图变量
'''
from App.views import blue_root, blue_user, blue_infer, blue_test

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
    app.register_blueprint(blueprint=blue_root)
    app.register_blueprint(blueprint=blue_user,url_prefix="/user")
    app.register_blueprint(blueprint=blue_infer,url_prefix="/infer")
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

    # 返回应用
    return app