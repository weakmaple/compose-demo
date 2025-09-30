import time
import redis
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
# 关键点：这里的 host='redis' 是我们 docker-compose.yml 文件中定义的 redis 服务的名字
# Docker Compose 会自动处理网络，让 webapp 容器能通过服务名找到 redis 容器
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            # cache.incr('hits') 会让 redis 里的 'hits' 这个键的值加 1
            # 如果键不存在，会先创建它并设为 1
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello, CI/CD! This is a new version. I have been seen {} times.'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

