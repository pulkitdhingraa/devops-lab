from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import redis
import time

app = Flask(__name__)

# Redis Client
r = redis.Redis(host="redis", port=6379, decode_responses=True)

# Metrics
jobs_submitted = Counter("jobs_submitted_total", "Total jobs inserted in redis queue")
redis_latency = Histogram("redis_command_latency_seconds", "Time spent in redis commands", ["command"])
http_request_total = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"])
http_request_duration = Histogram("http_request_duration_seconds", "Duration of HTTP requests", ["method", "endpoint"])

def timed_redis_call(cmd, *args, **kwargs):
    start = time.time()
    res = getattr(r, cmd)(*args, **kwargs)
    duration = time.time() - start
    redis_latency.labels(command=cmd).observe(duration)
    return res

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_http_metrics(response):
    duration = time.time() - request.start_time
    http_request_total.labels(request.method, request.path, response.status_code).inc()
    http_request_duration.labels(request.method, request.path).observe(duration)
    return response

@app.route("/submit", methods=["POST"])
def submit_job():
    payload = request.json
    timed_redis_call("rpush", "job_queue", str(payload))
    jobs_submitted.inc()
    return jsonify({"status": "queued"}), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)