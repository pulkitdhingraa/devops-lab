# Write a load_config() function for a trading service that reads these env vars:
# - EXCHANGE_API_KEY (required)
# - EXCHANGE_API_SECRET (required)
# - MAX_ORDER_SIZE (optional, default 10000, must be a positive float)
# - DRY_RUN (optional, default False)

# It should raise a clear EnvironmentError listing ALL missing required vars at once (not one by one). Return a typed dataclass.

import os
from dataclasses import dataclass

@dataclass
class Config:
    exchange_api_key: str
    exchange_api_secret: str
    max_order_size: float = 10000.0
    dry_run: bool = False

def load_config() -> Config:
    required = ["EXCHANGE_API_KEY", "EXCHANGE_API_SECRET"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise EnvironmentError(f"Missing required env vars: {missing}")
    
    max_order_size_raw = os.environ.get("MAX_ORDER_SIZE", "10000")
    try:
        max_order_size = float(max_order_size_raw)
    except ValueError:
        raise EnvironmentError(f"MAX_ORDER_SIZE must be a number, got: {max_order_size_raw}")
    if max_order_size <= 0:
        raise EnvironmentError(f"MAX_ORDER_SIZE must be positive, got: {max_order_size}")
    
    return Config(
        exchange_api_key = os.environ["EXCHANGE_API_KEY"],
        exchange_api_secret = os.environ["EXCHANGE_API_SECRET"],
        max_order_size = max_order_size,
        dry_run = os.environ.get("DRY_RUN", "false").lower() == "true"
    )

# Key Learnings

# Fail immediately with a clear message if config is wrong
# Failing fast at startup if required vars are missing
# [] for keys that exists and .get() for optional fields