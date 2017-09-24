import pytest

from rmon.models import Host

@pytest.fixture
def host():
    host = Host(name='redis_test', description='this is a test record',
                host='127.0.0.1', port='6379')
    host.save()
    return host
