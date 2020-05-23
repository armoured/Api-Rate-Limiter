# Fixed Window Api Rate Limiter for Python3

Hi, I created this Api Rate Limiter in Python3 using a Fixed Window Algorithm to improve my knowledge of distributed systems and put theory into practice. In the future I will modify this implementation to use a Sliding Window Algorithm to gain experience with extending exisitng software.

## Setup

The following setup instructions are for Mac (Linux will be similar.)

The application requires Python3, Pip, Virtualenv and Redis.

- Install Python3 and Pip from https://www.python.org/downloads/
- Install Redis from https://redis.io/topics/quickstart
- Install Virtualenv with `pip install virtualenv`

Now in the root of the project create a python virtual environment with
``virtualenv --python=`which python3` venv``

Then activate the virtualenv and install project dependencies from requirements.txt
```
source ./venv/bin/activate
pip install -r requirements.txt
```

## Run The Flask App

To see a quick example of the api rate limiter in action, there is an example flask app rate limited on the root route. The rate limiter in this example has been configured to allow a maximum of 3 requests every 20 seconds.

Firstly, start a redis server in a new terminal with
`redis-server`

Then in the original terminal run the flask app with

`python3 -m app.client.app`

Then navigate to http://127.0.0.1:5000/ in your preferred web browser.

Send requests to the server by reloading the page. After your 3rd reload within 20 seconds the api rate limiter will block your requests for the remainder of that window. The page will indicate whether you are blocked or not.

## Module Usage

The `RateLimiter` class has three callable functions that will allow you to rate limit your api's.

The constructor takes three arguments

- `key`: a unique identifier that is used as the key in the cache that keeps track of the number of requests a requestor has sent. IPV6 is an ideal identifier for a user. You can also specify a key that groups users, a key for the whole route or a key for the whole api.
- `max_reqs`: the maximum number of requests that a requestor can make within a specific time limit
- `time_limit`: the amount of time in seconds until the cached number of requests for a requestor is reset back to 0.

initialise a new instance of the rate limiter by 
`limiter = RateLimiter(key, max_reqs, time_limit)`

`limiter.is_blocked()`

The is_blocked function returns `true` if the requestor is blocked and `false` if the requestor is not. The function also increments the number of requests made by the requestor each call and checks if the requestor has made more requests than the maximum number of requests during the time limit.

`limiter.get_blocked_time()`

The get_blocked_time function returns the amount of time in seconds until the user becomes unblocked.

An example usage of this module is 
```
# Rate limit requestors to a maximum of 1000 requests every 10 minutes
# Status code 429 is returned when the rate limiter blocks a requestor

limiter = RateLimiter(key="Unique Key", max_reqs=1000, time_limit=600)
if limiter.is_blocked():
    return f"You are blocked. Please wait {limiter.get_blocked_time()} seconds.", 429

# Your api route business logic goes here
```

## Testing

From the root project directory make sure you have sourced your virtual environment with \
`source ./venv/bin/activate`

Then run \
`pytest -vs app/tests`

## System Design

This Api Rate Limiter has been implemented with a Fixed Window Algorithm. This allowed the implementation to be extremely simple. 

With a fixed window algorithm a requestor can send a certain amount of requests within a time period before they become rate limited.

A Redis cache is used to store the number of requests a user has sent during a fixed time period. Redis was chosen as it is a highly efficient key-value store ideal for this situation. 
It also provides atomicity in a distributed environment.

The Redis cache is hosted on a separate server. Using a cache on it's own server allows the rate limiter to be used across a cluster of servers, which means if a requestor sends more than the maximum number of requests on one server, they will be rate limited on all servers.


## Limitations and Enhancements

### Fixed Window Algorithm limitations

Fixed window algorithms are not entirely correct. For example, consider a maximum number of requests of 2 for a given fixed time window of 1 second. A requestor can send 2 requests just after 0.5 seconds, wait until 1 second has passed so they become unblocked and send another 2 requests before 1.5 seconds have passed. They have essentially sent 4 requests with a rolling time window of 1 second (1.5 seconds - 0.5 seconds) which is greater than the maximum of 2 requests per 1 second. 

This algorithm can generalise to worst case 2n requests being sent in a rolling time window the same amount of seconds as the fixed time window.

Redis limitations
 - spof
 - atomicity introduces more latency due to locking the cache when accessed.

Key choices IPV6 vs User Id/Token

