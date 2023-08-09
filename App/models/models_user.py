'''
在此处建立模型以及储存数据库对象
'''

from App.extensions import db

'''
模型 Model 类
必须继承 db.Model
'''

class UserModel(db.Model):
    '''
    用户类，存储用户名和密码
    '''
    # 表名
    __tablename__ = 'tb_user'
    # 表字段
    # db.Column是字段，db.Interger是整数,primary_key是主键，autoincrement是自动自增
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # db.String(30) 表示 varchar(30) 可变字符串；
    # unique 是不允许重复；
    # index 是索引，加快查询速度；
    # 用户的账户名
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    # 用户的姓名
    name = db.Column(db.String(30))
    # 电话
    contact = db.Column(db.String(50))
    # 保留字段，备注
    remark = db.Column(db.String(200))


class GinsengModel(db.Model):
    __tablename__ = 'tb_ginseng'
    ginseng_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 野山参图片文件名，它是对文件内容进行哈希运算后得到的
    ginseng_file_name = db.Column(db.String(100))
    # 检参时间
    ginseng_check_time = db.Column(db.DateTime)
    # 野山参等级
    ginseng_rank = db.Column(db.Integer)
    # 检验员，外键位于 tb_user 中
    inspector_id = db.Column(db.Integer,db.ForeignKey('tb_user.id'))
    # 可以通过 user.ginseng_inspected 访问该用户所检验过的所有野山参对象的列表
    # lazy 是懒加载，根据负载情况使用动态懒加载
    inspects = db.relationship('UserModel',backref=db.backref('ginseng_inspected',lazy='dynamic'))