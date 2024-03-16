from confluent_kafka import Producer


def delivery_report(err, msg):
    if err is not None:
        print(f"Topic creation failed: {err}")
    else:
        print(f"Topic {msg.topic()} created [{msg.partition()}]")


def create_topics():
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
    topics = ["auth-stream", "tracker-stream", "billing-stream"]

    for topic in topics:
        producer.produce(topic, callback=delivery_report)

    # Wait for message delivery
    producer.flush()


if __name__ == "__main__":
    create_topics()
