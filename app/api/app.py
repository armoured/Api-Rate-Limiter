from flask import Flask
import os
print (os.getcwd())
from ..limiter.limiter import RateLimiter
import time
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/test')
# @RateLimiter(id='mitch', max_reqs=3)
def test():
    limiter = RateLimiter('mitch', 3)
    if limiter.is_blocked():
        return f"You are blocked, please wait {limiter.get_blocked_time()} seconds", 429
    return "not blocked", 200


def main():
    for i in range(0, 70):
        print(test())
        time.sleep(1)

if __name__ == '__main__':
    main()
