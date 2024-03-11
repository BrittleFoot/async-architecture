from confluent_kafka import Producer


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def main():
    # Configure Kafka producer
    conf = {
        "bootstrap.servers": "localhost:9092",  # Kafka broker(s) address
        "client.id": "my_producer",  # Client ID for the producer
        "acks": "all",  # Wait for all replicas to acknowledge the message
        "retries": 3,  # Number of retries for failed message delivery
    }

    # Create Kafka producer instance
    producer = Producer(conf)

    # Produce messages
    topic = "auth-stream"

    value = "Init"
    producer.produce(topic, value.encode("utf-8"), callback=delivery_report)

    # Wait for message delivery
    producer.flush()


if __name__ == "__main__":
    main()
