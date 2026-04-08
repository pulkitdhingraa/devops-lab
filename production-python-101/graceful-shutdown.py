# Write a WorkerService class with:
# - A start() method that runs a loop processing jobs from a queue
# - Graceful shutdown on SIGTERM: finish the current job, stop taking new ones, log "shutdown complete"
# - A _process_job(job) stub method
# - The loop should sleep 0.5s between jobs

# Behave as if this runs inside a Kubernetes pod.

import logging
import time
import signal

log = logging.getLogger(__name__)
_shutdown = False

def _handle_shutdown(signum, frame):
    global _shutdown
    log.info("shutdown signal received", extra={"signal": signum})
    _shutdown = True

class WorkerService:
    def __init__(self):
        signal.signal(signal.SIGTERM, _handle_shutdown)
        signal.signal(signal.SIGINT, _handle_shutdown)

    def _get_next_job(self):
        pass

    def cancel_new_jobs(self):
        pass

    def _process_job(self, job):
        pass

    def start(self):
        log.info("processing jobs from queue")
        while not _shutdown:
            try:
                job = self._get_next_job()
                self._process_job(job)
            except Exception as e:
                log.error("job processing error", extra={"error": str(e)})
            time.sleep(0.5)

        log.info("shutdown: stopping new jobs")
        self.cancel_new_jobs()
        log.info("shutdown complete")


# Key Learnings

# Always handle SIGTERM
# Always finish the current unit of work before shutting down
# Run cleanup after the loop exits
# 30 seconds between SIGTERM and SIGKILL for K8
