""" rmon.common.decorators

该模块实现了装饰器
"""

from functools import wraps
from flask import request
from rmon.common.rest import RestException


class ObjectMustBeExist:
    """该装饰器确保操作的对象必须存在
    """

    def __init__(self, object_class):
        """
        Args:
            object_class (class): 数据库对象
        """

        self.object_class = object_class

    def __call__(self, func):
        """装饰器实现
        """
        @wraps(func)
        def wrapper(object_id, *args, **kwargs):
            """
            Args:
                object_id (int): SQLAlchemy object id
            """
            obj = self.object_class.query.get(object_id)
            if obj is None:
                raise RestException(404, 'not exist')
            request.instance = obj
            return func(object_id, *args, **kwargs)
        return wrapper


class cached_property:
    """缓存属性
    """
    pass
