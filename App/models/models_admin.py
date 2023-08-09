from App.extensions import db

class AdminUserModel(db.Model):
    __tablename__ = 'tb_adminuser'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    # 管理员的姓名
    name = db.Column(db.String(30))
    # 管理员的电话
    contact = db.Column(db.String(50))
    # 保留字段，备注
    remark = db.Column(db.String(200))