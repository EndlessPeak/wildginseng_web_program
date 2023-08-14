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
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    # 用户的姓名
    name = db.Column(db.String(10))
    # 电话
    contact = db.Column(db.String(50))
    # 保留字段，备注
    remark = db.Column(db.String(200))

class GinsengInferModel(db.Model):
    '''
    野山参推理表
    该表保存单次由野山参图片推理得到的结果
    '''
    __tablename__ = 'tb_ginseng_infer'
    ginseng_infer_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 野山参的ID，外键位于 tb_ginseng 中
    ginseng_id = db.Column(db.Integer,db.ForeignKey('tb_ginseng.id'))
    # 野山参该次推理所使用的图片的文件名，它是对文件内容进行哈希运算后得到的
    ginseng_file_name = db.Column(db.String(100))
    # 检参时间，包含年、月、日、时、分、秒数据
    ginseng_check_time = db.Column(db.DateTime)
    # 野山参该次推理得到的等级信息
    ginseng_rank = db.Column(db.Integer)
    # 可以通过 ginseng.ginseng_infered 访问该野山参所经过检验的所有野山参图片的列表
    # lazy 是懒加载，根据负载情况使用动态懒加载
    infers = db.relationship('GinsengModel',backref=db.backref('ginseng_infered',lazy='dynamic'))

class GinsengModel(db.Model):
    '''
    野山参表，保存每个野山参的数据
    '''
    __tablename__ = 'tb_ginseng'
    # 野山参的ID
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 野山参的综合等级信息，采用多数表决方法
    ginseng_rank = db.Column(db.Integer)
    # 检验员，外键位于 tb_user 中
    inspector_id = db.Column(db.Integer,db.ForeignKey('tb_user.id'))
    # 可以通过 user.ginseng_inspected 访问该用户所检验过的所有野山参图片的列表
    # lazy 是懒加载，根据负载情况使用动态懒加载
    inspects = db.relationship('UserModel',backref=db.backref('ginseng_inspected',lazy='dynamic'))