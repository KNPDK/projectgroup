import time
import os
import redis
from flask import Flask, render_template

template_dir = os.path.abspath('view/templates')
app = Flask(__name__, template_folder=template_dir);
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('index.html', c=format(count))


@app.route('/chat')
def chat():
    return render_template('chat.html')
