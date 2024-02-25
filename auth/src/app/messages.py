import json
import os
from typing import TypedDict

from confluent_kafka import Producer as KafkaProducer


class Event(TypedDict):
    event: str
    data: dict
    id: str


class Topics:
    ACCOUNT = "account"


class UserEvents:
    CREATED = "user.created"
    UPDATED = "user.updated"

    @staticmethod
    def wrap(event, data) -> Event:
        assert "id" in data, "Data must contain an id field"
        return Event(
            event=event,
            data=data,
            id=str(data["id"]),
        )


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
            print(">>> Message delivery failed: {}".format(err))
        else:
            print(">>> Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

    def produce(self, topic, messages: list[Event]):
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
