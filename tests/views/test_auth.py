""" tests.views.test_auth

登录认证功能测试
"""

from flask import url_for

from rmon.models import User
from tests.fixtures import PASSWORD


class TestAuth:
    """测试登录功能

    登录成功后将获取到用于访问各项 API 的 token
    """

    endpoint = 'api.login'

    def test_login_success(self, client, user):
        """登录成功
        """

        data = {'name': user.name, 'password': PASSWORD}

        resp = client.post(url_for(self.endpoint), data=data)

        assert resp.status_code == 200
        assert resp.json['ok'] == True

        # 获取到的 token 成功验证
        u = User.verify_token(resp.json['token'])

        assert u == user

