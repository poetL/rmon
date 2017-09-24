""" rmon.model

该模块实现了所有的 model 类以及相应的序列化类
"""
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from marshmallow import (Schema, fields, validate, post_load,
                         validates_schema, ValidationError)
from redis import StrictRedis, RedisError

from rmon.common.rest import RestException

db = SQLAlchemy()


class Host(db.Model):
    """Redis服务器
    """

    __tablename__ = 'redis_host'

    id = db.Column(db.Integer, primary_key=True)
    # unique = True 设置不能有同名的服务器
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(512))
    host = db.Column(db.String(15))
    port = db.Column(db.Integer, default=6379)
    password = db.Column(db.String())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        """保存到数据库中
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """从数据库中删除
        """
        db.session.delete(self)
        db.session.commit()

    @property
    def redis(self):
        return StrictRedis(host=self.host, port=self.port, password=self.password)

    def ping(self):
        """检查 Redis 服务器是否可以访问
        """
        try:
            self.redis.ping()
        except RedisError:
            raise RestException(400, 'redis server %s can not connected' % self.host)

    def get_metrics(self):
        """获取 Redis 服务器监控信息
        """
        try:
            # TODO 新版本的 Redis 服务器支持查看某一 setion 的信息，不必返回所有信息
            return self.redis.info()
        except RedisError:
            raise RestException(400, 'redis server %s can not connected' % self.host)

    def execute(self, *args, **kwargs):
        """执行命令
        """
        pass


class HostSchema(Schema):
    """Redis服务器记录序列化类
    """
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(2, 64))
    description = fields.String(validate=validate.Length(0, 512))
    # host 必须是 IP v4 地址
    host = fields.String(required=True,
                         validate=validate.Regexp(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))
    port = fields.Integer(required=True, validate=validate.Range(1024, 65536))
    password = fields.String()
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_host(self, data):
        """验证是否已经存在同名 Redis 服务器
        """
        instance = self.context.get('instance', None)
        if instance is None:
            return

        host = Host.query.get(data['host'])
        if host is None:
            return

        if host == instance:
            raise ValidationError('host already exist', 'host')

    @post_load
    def create_or_update(self, data):
        """数据加载成功后自动创建 Host 对象
        """
        instance = self.context.get('instance', None)
        # 创建 Redis 服务器
        if instance is None:
            return Host(**data)

        # 更新服务器
        for key in data:
            setattr(instance, key, data['key'])
        return instance
