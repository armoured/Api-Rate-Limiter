# Fixed Window Api Rate Limiter for Python3

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

The RateLimiter class has three callable functions that will allow you to rate limit your api's.

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

## Limitations and Enhancements