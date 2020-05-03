from limiter.limiter import RateLimiter
import time

# @RateLimiter(id='mitch', threshold=3)
def lambda_handler(event, context):
    print("TODO", event, context)
    limiter = RateLimiter('mitch', 3)
    if limiter.is_blocked():
        print("You are blocked")
        return
    print("not blocked")


def main():
    for i in range(0, 70):
        lambda_handler(0,1)
        time.sleep(1)

if __name__ == '__main__':
    main()
