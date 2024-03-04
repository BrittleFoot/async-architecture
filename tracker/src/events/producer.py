import logging
import os

from confluent_kafka import Producer as KafkaProducer
from jirapopug.schema.message import BaseData, Message

logger = logging.getLogger(__name__)


class Producer:
    def __init__(self, name: str):
        self.name = name
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
            logger.error(f"Message delivery failed: {err}")
            return

        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send[T: BaseData](self, messages: list[T]):
        for event in messages:
            self.kp.poll(0)

            message = Message[T](producer=self.name, data=event)
            raw_data = message.model_dump_json()
            self.kp.produce(
                topic=event.__topic__,
                key=event.public_id,
                value=raw_data.encode("utf-8"),
                callback=self.delivery_report,
            )

        self.kp.flush()
