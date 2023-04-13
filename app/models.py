# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField,PrimaryKeyField,FloatField
import json
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager
from conf.config import config
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)


# 管理员工号
class User(UserMixin, BaseModel):
    username = CharField()  # 用户名
    password = CharField()  # 密码
    fullname = CharField()  # 真实性名
    email = CharField()  # 邮箱
    phone = CharField()  # 电话
    status = BooleanField(default=True)  # 生效失效标识

    def verify_password(self, raw_password):
        return self.password == raw_password

# 家具类型
class FurnitureType(BaseModel):
    furnitureType = PrimaryKeyField()   #类型ID
    typeENName = CharField()  # 类型英文
    typeCHName = CharField()  # 类型中文

# 家具风格
class FurnitureStyles(BaseModel):
    furnitureStyle = PrimaryKeyField()   #风格ID
    name = CharField()  # 风格名

# 家具风格2
class FurnitureType2(BaseModel):
    furnitureType = PrimaryKeyField()   #类型ID
    furnitureType2 = IntegerField()   #类型2ID
    typeENName = CharField()  # 类型英文
    typeCHName = CharField()  # 类型中文

# 供应商
class Organizations(BaseModel):
    organizationID = PrimaryKeyField()   #供应商ID
    organizationName = CharField()  # 供应商名称


# 通知人配置
class FurnituresData(BaseModel):
    furnitureID = CharField()  # 家具的唯一ID
    uploadUserID = IntegerField()  # 上传用户的ID
    organization = CharField()  # 上传组织
    furnitureType = IntegerField()  # 上传家具一级类型
    furnitureType2 = IntegerField()  # 上传家具二级类型
    furniturePicUrl = CharField()    # 上传家具缩略图地址
    brand = CharField()    # 上传家具的品牌
    furnitureName = CharField()    # 上传家具的名称
    furnitureMarking = CharField()    # 上传模型的型号
    furnitureCraft = CharField()    # 上传模型的工艺
    furnitureColor = CharField()    # 上传模型的颜色
    furnitureStyle = IntegerField()   #模型风格
    furniturePurePrice = FloatField()   #模型售价

@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))


# 建表
def create_table():
    db.connect()
    db.create_tables([FurnituresData, User])


if __name__ == '__main__':
    create_table()
