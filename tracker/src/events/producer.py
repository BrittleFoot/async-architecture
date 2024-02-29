import json
import logging
import os

from confluent_kafka import Producer as KafkaProducer

from events.types import DataMessage

logger = logging.getLogger(__name__)


class Producer:
    def __init__(self):
        self.kp = KafkaProducer(
            {
                "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            }
        )

    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush().
        """
        if err is not None:
            logger.warning("Message delivery failed: %s", err)
            return

        logger.info("Message delivered to %s [%s]", msg.topic(), msg.partition())

    def produce(self, topic, messages: list[DataMessage]):
        for event in messages:
            self.kp.poll(0)

            data = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
            self.kp.produce(
                topic=topic,
                key=event["id"],
                value=data.encode("utf-8"),
                callback=self.delivery_report,
            )

        self.kp.flush()
