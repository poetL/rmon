from rmon.models import Host
from rmon.common.rest import RestException

class TestHost:
    """测试 Host 相关功能
    """

    def test_save(self, db):
        """测试 Host.save 保存服务器方法
        """
        # 初始状态下，数据库中没有保存任何 Redis，所以数量为 0
        assert Host.query.count() == 0
        host = Host(name='test', host='127.0.0.1')
        # 保存到数据库中
        host.save()
        # 现在数据库中数量变为 1
        assert  Host.query.count() == 1
        # 且数据库中的记录就是之前创建的记录
        assert Host.query.first() == host

    def test_delete(self, db, host):
        """测试 Host.delete 删除服务器方法
        """
        assert Host.query.count() == 1
        host.delete()
        assert Host.query.count() == 0

    def test_ping_success(self, db, host):
        """测试 Host.ping 方法执行成功

        需要保证 Redis 服务器监听在 127.0.0.1:6379 地址
        """
        assert host.ping() is True

    def test_ping_failed(self, db):
        """测试 Host.ping 方法执行失败

        Host.ping 方法执行失败时，会抛出 RestException 异常
        """

        # 没有 Redis 服务器监听在 127.0.0.1:6399 地址, 所以将访问失败
        host = Host(name='test', host='127.0.0.1', port=6399)

        try:
            host.ping()
        except RestException as e:
            assert e.code == 400
            assert e.message == 'redis server %s can not connected' % host.host

    def test_get_metrics_success(self, host):
        """测试 Host.get_metrics 方法执行成功
        """

        metrics = host.get_metrics()

        # refer https://redis.io/commands/INFO
        assert 'total_commands_processed' in metrics
        assert 'used_cpu_sys' in metrics
        assert 'used_memory' in metrics

    def test_get_metrics_failed(self, host):
        """ 测试 Host.get_metrics 方法执行失败
        """

        # 没有 Redis 服务器监听在 127.0.0.1:6399 地址, 所以将访问失败
        host = Host(name='test', host='127.0.0.1', port=6399)

        try:
            info  = host.get_metrics()
        except RestException as e:
            assert e.code == 400
            assert e.message == 'redis server %s can not connected' % host.host