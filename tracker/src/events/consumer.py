import json
import os
from typing import Callable

from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaError, KafkaException, Message
from django.core.management.base import BaseCommand

from events.types import DataMessage


class Consumer:
    def __init__(
        self,
        topics: list[str],
        message_handlers: dict[tuple[str, str], Callable[[DataMessage], None]],
        command: BaseCommand,
    ):
        self.topics = topics
        self.message_handlers = message_handlers
        self.command = command
        self.running = False

        self._consumer = KafkaConsumer(
            {
                "bootstrap.servers": os.getenv("KAFKA_BROKER"),
                "group.id": os.getenv("KAFKA_GROUP_ID"),
                "auto.offset.reset": "earliest",
                "enable.auto.commit": False,
            }
        )

    def warn(self, message: str):
        self.command.stdout.write(self.command.style.WARNING(message))

    def process(self, msg: Message):
        topic = msg.topic()
        message_value = msg.value()
        try:
            data = DataMessage(**json.loads(message_value))
        except json.JSONDecodeError:
            self.warn(
                f"Could not decode message value from topic {topic}: {message_value}"
            )
            return
        except TypeError:
            self.warn(f"Invalid message format from topic {topic}: {message_value}")
            return

        handler_key = (topic, data["event"])

        if handler_key not in self.message_handlers:
            raise KafkaException(f"No handler for event {handler_key}")

        handler = self.message_handlers[handler_key]

        # DO NOT CATCH EXCEPTIONS HERE
        # Let the consumer crash and restart
        # Better to crash and restart than to lose messages
        handler(data)

    def begin_consume(self):
        self.running = True
        try:
            self.command.stdout.write(
                self.command.style.SUCCESS(f"Subscribing to topics: {self.topics}")
            )
            self._consumer.subscribe(list(self.topics))

            while self.running:
                msg = self._consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if error := msg.error():
                    if error.code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        self.warn(
                            f"% {msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}\n"
                        )
                        continue

                    raise KafkaException(error)

                #################
                self.process(msg)
                #################
                self._consumer.commit(message=msg, asynchronous=False)
                ######################################################

        except KeyboardInterrupt:
            self.warn("Received keyboard interrupt. Shutting down...")
        finally:
            # commit final offsets.
            self._consumer.close()

    def shutdown(self):
        self.running = False
