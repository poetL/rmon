""" rmon.views.wx

微信相关视图控制器
"""
import hashlib

from flask import request, current_app, abort, render_template, g, make_response
from flask.views import MethodView
from wechatpy import parse_message, create_reply

from rmon.common.errors import RestError
from rmon.common.rest import RestView

from .decorators import TokenAuthenticate


class WxView(MethodView):
    """ 微信相关视图控制器
    """

    def check_signature(self):
        """ 验证请求是否来自于微信请求
        """
        signature = request.args.get('signature')
        if signature is None:
            abort(403)

        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')

        msg = [current_app.config['WX_TOKEN'], timestamp, nonce]
        msg.sort()

        sha = hashlib.sha1()
        sha.update(''.join(msg).encode('utf-8'))

        if sha.hexdigest() != signature:
            abort(403)

    def get(self):
        """ 用于验证在微信公众号后台设置的URL
        """
        self.check_signature()
        return request.args.get('echostr')

    def post(self):
        """ 处理微信消息
        """
        self.check_signature()

        msg = parse_message(request.data)
        reply = create_reply('实验楼, rmon', msg)
        return reply.render()


class WxBind(RestView):
    """微信注册绑定账户页面
    """

    # 只有 POST 方法才需要认证
    method_decorators = {'post': TokenAuthenticate()}

    def get(self):
        result = render_template('wx_bind.html')
        return make_response(result, 200)

    def post(self):
        """绑定用户
        """
        data = request.get_json()
        if data is None or 'wx_id' not in data:
            raise RestError(400, 'not found wx id')
        g.user.wx_id= data.get('wx_id')
        g.user.save()
        return {'ok': True, 'message': 'bind success'}

