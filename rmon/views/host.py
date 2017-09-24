""" rmon.views.host

实现了所有的视图控制器
"""
from flask import request
from flask.views import MethodView

from rmon.common.rest import RestView
from rmon.common.decorators import ObjectMustBeExist
from rmon.models import Host, HostSchema

class HostList(RestView):
    """Redis 服务器列表
    """

    def get(self):
        """获取 Redis 列表
        """
        hosts = Host.query.all()
        return HostSchema().dump(hosts, many=True).data

    def post(self):
        """创建 Redis 实例
        """
        data = request.get_json()
        host, errors = HostSchema().load(data)
        if errors:
            return errors, 400
        host.ping()
        host.save()
        return {'ok': True}, 201


class HostDetail(MethodView):
    """ Redis 服务器列表
    """

    method_decorators = (ObjectMustBeExist(Host), )

    def get(self, host_id):
        """
        """
        data, _ = HostSchema().dump(request.instance)
        return data

    def put(self, host_id):
        """更新服务器
        """
        schema = HostSchema(context={'instance': request.instance})
        data = request.get_json()
        host, errors = schema.load(data, partial=True)
        if errors:
            return errors, 400
        host.save()
        return {'ok': True}

    def delete(self, host_id):
        """删除服务器
        """
        request.instance.delete()
        return {'ok': True}, 204


class HostMetrics(RestView):
    """获取服务器监控信息
    """
    method_decorators = (ObjectMustBeExist(Host), )

    def get(self, host_id):
        """获取监控信息
        TODO 如何限制访问频率
        """
        return request.instance.get_metrics()


class HostCommand(RestView):
    """执行命令
    """

    method_decorators = (ObjectMustBeExist(Host), )

    def post(self, host_id):
        """执行 Redis 命令
        TODO 命令参数如何解析
        """
        pass
