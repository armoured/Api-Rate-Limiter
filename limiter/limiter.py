import redis
import time

ONE_MINUTE = 60

class RateLimiter:

    def __init__(self, id, threshold):
        self.id = id
        self.threshold = threshold
        self.store = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

    def __call__(self, f):
        def wrapper(*args):
            if self.is_blocked():
                print("You are blocked")
                return
            print("not blocked")
            f(*args)
        return wrapper
    
    def is_blocked(self):
        """
        Returns true if user is blocked and false if user is not blocked
        """
        current_time = int(time.time())
        # record = self.store.hgetall(self.id)
        record = self.hgetall()

        # Allow if this is the first request for the id or the last request
        # was sent a minute or more ago
        if not record or current_time - record["time"] >= ONE_MINUTE:
            self.store.hmset(self.id, {
                "count": 1,
                "time": current_time
            })
            return False

        # Allow if this request hasn't reach the maximum number of requests
        if record["count"] < self.threshold:
            self.store.hincrby(self.id, "count")
            self.store.hset(self.id, "time", current_time)
            return False

        # reject request
        return True

    def hgetall(self):
        return {
            k: int(v) for k, v in self.store.hgetall(self.id).items()
        }
        
        
            

        


    