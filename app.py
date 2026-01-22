from flask import Flask
import time
import redis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                return "Cannot connect to DB"
            retries -= 1
            time.sleep(0.5)
@app.route('/')
def hello():
    count = get_hit_count()
    if isinstance(count, str):
        return f"Hello World! (DB error: {count})"
    return f"Hello World! I have been seen {count} times."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)