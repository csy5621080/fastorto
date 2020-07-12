from aredis import StrictRedis


def redis_cli():
    client = StrictRedis(host='127.0.0.1', port=6379, db=0)
    return client


redis_client = redis_cli()