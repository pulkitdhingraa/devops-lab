## Topic Management

#### Create a topic
```
kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 2
```

#### List topics
```
kafka-topics.sh --list --bootstrap-server localhost:9092
```

#### Describe a topic
```
kafka-topics.sh --describe --topic test-topic --bootstrap-server localhost:9092
```

#### Delete a topic
```
kafka-topics.sh --delete --topic test-topic --bootstrap-server localhost:9092
```

## Produce & Consume Messages

#### Produce messages
```
kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092
```

#### Consume messages
```
kafka-console-consumer.sh --topic test-topic --bootstrap-serve localhost:9092 --from-beginning
```

#### Consume with key & timestamp
```
kafka-console-consumer.sh --topic test-topic --bootstrap-server localhost:9092 --from-beginning --property print.key=true --property print.timestamp=true
```

## Consumer Groups & Offsets

#### List consumer groups
```
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

#### Describe a consumer group
```
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --describe
```

#### Reset offsets to earliest
```
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --topic test-topic --reset-offsets --to-earliest --execute
```

## Cluster / Broker Info

#### List brokers (ZooKeeper)

```
zookeeper-shell.sh localhost:2181 ls /brokers/ids
```

#### Broker metadata
```
kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

#### Cluster metadata (KRaft mode)
```
kafka-metadata-shell.sh --bootstrap-server localhost:9092
```

## Debug/Maintenance

#### View topic messages with key, value, timestamp
```
kafka-console-consumer.sh --topic test-topic --bootstrap-server localhost:9092 --from-beginning --property print.key=true --property print.value=true --property print.timestamp=true
```

#### Delete local Kafka data (for testing)
```
rm -rf /tmp/kafka-logs /tmp/zookeeper
```

## kcat commands

#### Produce Messages
```
kcat -b localhost:9092 -t test-topic -P
```

#### Consume Messages
```
kcat -b localhost:9092 -t test-topic -C -o beginning
```

#### Consume With Offsets
```
kcat -b localhost:9092 -t test-topic -p 0 -o beginning -C -q
```

#### List Metadata
```
kcat -L -b localhost:9092
```