import hashlib
from flask import request, current_app, abort
from flask.views import MethodView
from wechatpy import parse_message, create_reply


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
