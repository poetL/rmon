""" app.py

应用入口文件
"""
import urllib
from rmon.app import create_app

app = create_app()

@app.cli.command()
def routes():
    """输出 app 中定义的所有路由
    """
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:25s} {:35s} {:20s}".format(
            rule.endpoint, methods, str(rule)))
        output.append(line)

    for line in sorted(output):
        print(line)
