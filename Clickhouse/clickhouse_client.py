import clickhouse_connect


def clickhouse_client():
    return clickhouse_connect.get_client(host='localhost', username='default')


