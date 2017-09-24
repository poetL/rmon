""" rmon.common.json

该模块基于 flask.json.JSONDecoder 实现了 json 序列化工具。
"""
from datetime import datetime

from flask.json import JSONDecoder

class CustomJSONEncoder(JSONDecoder):
    """自定义 json 编码器
    """

    def default(self, obj):
        """覆盖父类方法
        """
        # 如果是 datetime 类型，则转换为时间字符串
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')

        if hasattr(obj, 'keys') and hasattr(o, '__getitem__'):
            return dict(obj)

        return super(CustomJSONEncoder, self).default(obj)
