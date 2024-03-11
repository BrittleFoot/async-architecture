import json
import os
from typing import Type

import pydantic
from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaError, KafkaException
from confluent_kafka import Message as KafkaMessage
from django.core.management.base import BaseCommand
from jirapopug.schema.message import BaseData, Message

from events.types import TopicHander, TopicKey


class Consumer:
    def __init__(
        self,
        topics: list[str],
        message_handlers: dict[TopicKey, TopicHander],
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

    def handle_error(self, error: KafkaError):
        if error.code() == KafkaError._PARTITION_EOF:
            # End of partition event
            self.warn(
                f"% {error.topic()} [{error.partition()}] reached end at offset {error.offset()}\n"
            )
            return
        raise KafkaException(error)

    def parse_message(self, topic: str, message_value: str) -> Message[dict]:
        try:
            message = json.loads(message_value)
            return Message[dict].model_validate(message)

        except json.JSONDecodeError:
            self.warn(
                f"Could not decode message value from topic {topic}: {message_value}"
            )
        except pydantic.ValidationError as e:
            self.warn(f"Invalid message format from topic {topic}: {message_value}")
            raise e

    def parse_data(
        self, topic: str, message: Message[dict], schema_version=Type[BaseData]
    ) -> BaseData:
        try:
            return schema_version.model_validate(message.data)

        except json.JSONDecodeError:
            self.warn(f"Could not decode message value from topic {topic}: {message}")
        except TypeError as e:
            self.warn(f"Invalid message format from topic {topic}: {message}")
            self.warn(f"Error: {e}")

    def process(self, msg: KafkaMessage):
        topic = msg.topic()
        message_value = msg.value()

        message = self.parse_message(topic, message_value)
        if message is None:
            return

        handler_key = TopicKey(topic, message.event_name, message.event_version)

        if handler_key not in self.message_handlers:
            """ We raise an exception here because we want the consumer to crash and restart
            In real world scenarios, we would want to log this error and possibly
            add it to a dead letter queue for further analysis
            """
            raise KafkaException(f"No handler for event {handler_key}")

        topic_handler = self.message_handlers[handler_key]

        data = self.parse_data(topic, message, topic_handler.schema_version)
        if data is None:
            return

        # DO NOT CATCH EXCEPTIONS HERE
        # Let the consumer crash and restart
        # Better to crash and restart than to lose messages for now
        topic_handler.func(data)

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
                    self.handle_error(error)
                    continue

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
