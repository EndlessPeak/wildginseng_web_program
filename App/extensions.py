'''
扩展插件管理

导入第三方插件
1. SQLAlchemy
2. Migrate
'''
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

'''
初始化
'''
db = SQLAlchemy()
migrate = Migrate()

def init_extensions(app):
    db.init_app(app=app)
    migrate.init_app(app=app,db=db)
    