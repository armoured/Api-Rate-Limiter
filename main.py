from limiter.limiter import RateLimiter
import time

# @RateLimiter(id='mitch', threshold=3)
def api_call(a, b):
    print("TODO", a, b)
    limiter = RateLimiter('mitch', 3)
    if limiter.is_blocked():
        print("You are blocked")
        return
    print("not blocked")


def main():
    for i in range(0, 70):
        api_call(0,1)
        time.sleep(1)

if __name__ == '__main__':
    main()

