# Write a retry decorator that supports:
# - max_attempts: how many times to try
# - on_retry: optional callback(attempt, error) called before each retry
# - Exponential backoff: delay doubles each attempt
# - Only retries on the exception types passed in

# Then use it to decorate a function publish_to_kafka(topic, message) that retries on KafkaTimeoutError up to 5 times and logs each retry attempt via the callback.

from functools import wraps
import random
import time
import logging
import requests
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError

log = logging.getLogger(__name__)

def retry(max_attempts=3, base_delay=1.0, exceptions=(Exception,), on_retry=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts+1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        log.error("max retries exceeded", extra={"fn": fn.__name__, "error": str(e)})
                        raise
                    if on_retry:
                        on_retry(attempt, e)
                    delay = base_delay * (2 ** (attempt-1)) + random.uniform(0,0.5)
                    log.warning("retrying", extra={"fn": fn.__name__, "attempt": attempt, "delay" : round(delay,2)})
                    time.sleep(delay)
        return wrapper
    return decorator

def log_retry(attempt: int, error: Exception) -> None:
    log.warning("kafka retry", extra={"attempt": attempt, "error": str(error)})

@retry(max_attempts=5, base_delay=0.5, exceptions=(KafkaTimeoutError,), on_retry=log_retry)
def publish_to_kafka(topic: str, message: str) -> None:
    log.info("publishing message", extra={"topic": topic})
    producer = KafkaProducer(bootstrap_servers="localhost:9092")
    producer.send(topic, message.encode("utf-8"))
    producer.flush()
    log.info("message published", extra={"topic": topic})



# Key Learnings

# Exponential backoff with jitter
# Retry only on transient errors (network timeouts, 5xx)
# Set max retry count
# Always log retry attempts
# Write own decorator functions