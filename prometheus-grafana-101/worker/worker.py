from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import redis
import time
import random
import threading

app = Flask(__name__)

# Redis Client
r = redis.Redis(host="redis", port=6379, decode_responses=True)

# Metrics
jobs_processed = Counter("jobs_processed_total", "Total jobs processed")
jobs_failed = Counter("jobs_failed_total", "Total jobs failed", ["reason"])
job_latency = Histogram("job_latency_seconds", "Time spent processing the job")
queue_depth = Gauge("redis_queue_depth", "Number of jobs in redis queue")
redis_latency = Histogram("redis_command_latency_seconds", "Time spent in redis commands", ["command"])

def timed_redis_call(cmd, *args, **kwargs):
    start = time.time()
    res = getattr(r, cmd)(*args, **kwargs)
    duration = time.time() - start
    redis_latency.labels(command=cmd).observe(duration)
    return res

def job_worker():
    while True:
        job = timed_redis_call("lpop", "job_queue")
        queue_depth.set(r.llen("job_queue"))
        
        if not job:
            time.sleep(0.1)
            continue
        
        start = time.time()
        time.sleep(random.uniform(0.05, 0.3))
        duration = time.time() - start
        job_latency.observe(duration)

        rnd = random.random()
        if rnd < 0.1:
            jobs_failed.labels(reason="invalid_data").inc()
        elif rnd < 0.2:
            jobs_failed.labels(reason="timeout").inc()
        else:  
            jobs_processed.inc()
        
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    t = threading.Thread(target=job_worker, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=6000)