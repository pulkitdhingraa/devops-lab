**Build a containerized Kafka cluster with a frontend and monitoring stack to observe the effect of degraded network conditions on message latency and throughput when one broker becomes slow.**


#### 1. Env Setup 
- Deploy env with docker compose
    - Zookeper
    - Kafka brokers
    - nginx frontendub
    - prometheus+grafana
- Nginx Config files that proxy kafka cluster

#### 2. Traffic Simulation
- Use tc(traffic control) to introduce artificial latency or packet loss on one of the kafka broker container 

#### 3. Produce/Consume Test
- Use kcat (CLI kafka client) to send and receive msgs while observing latency
    - Create topics
    - produce msgs
    - consume msgs
    - observe throughput


#### 4. Monitoring & Visualization
- Add kafka exporter
- Grafana dashboard showing how one broker's latency propagates through kafka streams

#### 5. Observations
- Increased replication lag
- Cause ISR(In-Sync Replicas) shrinkage
- Delay message ack
- Reduce overall consumer throughput

#### 6. Prevention
- Broker isolation
- Auto detect and remove degraded broker (self-heal)
- Client level fault tolerance