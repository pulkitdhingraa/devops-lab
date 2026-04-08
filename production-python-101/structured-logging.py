# Write a Python function called check_service_health(service_name, url) that:
# - Logs at INFO level when starting the check
# - Logs at WARNING if the response time exceeds 500ms
# - Logs at ERROR with the exception details if the request fails
# - Uses the logging module, not print()


import logging
import sys
import requests
import time

logging.basicConfig(stream=sys.stdout,level=logging.INFO,format='{"time":"%(asctime)s", "level":"%(levelname)s", "msg":"%(message)s"}')

log = logging.getLogger("service-health")

def check_service_health(service_name: str, url: str):
  log.info("starting the check", extra={"service_name": service_name, "url": url})
  try:
    start = time.time()
    response = requests.get(url, timeout=5)
    elapsed_ms = (time.time() - start) * 1000
    if elapsed_ms > 500:
      log.warning("response time exceeds 500ms", extra={"service_name": service_name, "url": url})
  except Exception as e:
    log.error("request failed", extra={"service_name": service_name, "url": url, "error": str(e)})
    raise
  
# Key Learnings

# Use logging module
# Every log line should be answerable as a structured query
# Never return None always raise
# Every log should be traceable back to action