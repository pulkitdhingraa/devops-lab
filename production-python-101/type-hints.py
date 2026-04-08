# Model a Kubernetes pod event for a monitoring system. Create:
# - A dataclass PodEvent with: pod_name (str), namespace (str), event_type (str), timestamp (float), message (str), node_name (Optional[str])
# - A dataclass AlertRule with: name (str), severity (str), keywords (list[str])
# - A function matches_alert(event: PodEvent, rule: AlertRule) -> bool that returns True if any keyword appears in the event message (case-insensitive)

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class PodEvent:
    pod_name: str
    namespace: str
    event_type: str
    timestamp: float
    message: str
    node_name: Optional[str] = None

@dataclass
class AlertRule: 
    name: str
    severity: str
    keywords: list[str]

def matches_alert(event: PodEvent, rule: AlertRule) -> bool:
    for keyword in rule.keywords:
        if keyword.lower() in event.message.lower():
            return True

    return False
    # return any(kw.lower() in event.message.lower() for kw in rule.keywords)


######## Another example #########
@dataclass
class Trade:
    id: str
    symbol: str
    side: str # "buy" or "sell"
    qty: float
    price: float

@dataclass
class TradeResult: 
    trade_id: str
    status: str
    value: float
    error: Optional[str] = None

@dataclass
class ProcessingConfig:
    min_qty: float = 0.01
    allowed_symbols: list[str] =  field(default_factory=list) # mutable default arguments are shared across all instances. So cannot initialize with [] or list()

def process_trades(trades: list[Trade], config: ProcessingConfig) -> list[TradeResult]:
    results: list[TradeResult] = []
    for trade in trades:
        if trade.side == "buy" and trade.qty >= config.min_qty:
            results.append(TradeResult(
                trade_id=trade.id,
                status="processed",
                value=trade.qty*trade.price
            ))
    return results

# Key Learnings

# Annotate all function signatures
# Use dataclasses for data containers
# Use Optional[T] for nullable values
# Use list[T] and dict[K, V] for collections