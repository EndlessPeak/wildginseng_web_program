'''
@Author EndlessPeak
@Data 2023/8/8
在本文件中创建flask应用
'''

'''
导入flask框架，这将包含以下内容:
1. Flask
2. render_template
3. session
4. request
5. send_from_directory
6. jsonify 用于json数据序列化，将数据对象变成json字符串  
'''
from flask import Flask,render_template,session,request,send_from_directory,jsonify
from App.views import blue_root

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

    # 返回应用
    return app