'''
在此处建立模型以及储存数据库对象
'''

from App.extensions import db

'''
模型 Model 类
必须继承 db.Model
'''
class User(db.Model):
    # 表名
    __tablename__ = 'tb_user'
    # 表字段
    # db.Column是字段，db.Interger是整数,primary_key是主键，autoincrement是自动自增
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # db.String(30) 表示 varchar(30) 可变字符串, index是索引，加快查询速度
    name = db.Column(db.String(30), unique=True,index=True)