""" rmon.views.urls

定义了所有 API 对应的 URL
"""
from flask import Blueprint

from rmon.views.host import HostList, HostDetail, HostMetrics, HostCommand
from rmon.views.index import IndexView


api = Blueprint('api', __name__, url_prefix='/')

api.add_url_rule('/', view_func=IndexView.as_view('index'))

api.add_url_rule('/hosts/', view_func=HostList.as_view('host_list'))
api.add_url_rule('/hosts/<host_id>', view_func=HostDetail.as_view('host_detail'))
api.add_url_rule('/hosts/<host_id>/metrics', view_func=HostMetrics.as_view('host_metrics'))
api.add_url_rule('/hosts/<host_id>/command', view_func=HostCommand.as_view('host_command'))
