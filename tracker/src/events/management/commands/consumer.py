import logging

from django.core.management.base import BaseCommand

from events.consumer import Consumer
from events.handlers import REGISTERED_TOPIC_HANDLERS, REGISTERED_TOPICS


class Command(BaseCommand):
    help = "Starts the Kafka consumer"

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="[%(levelname)s][%(topic)s][%(event)s][%(func)s] %(message)s",
        )

    def handle(self, *args, **options):
        self.setup_logging()

        self.stdout.write(self.style.SUCCESS("Starting Kafka consumer..."))

        if not REGISTERED_TOPIC_HANDLERS:
            self.stdout.write(
                self.style.WARNING(
                    "No topic handlers have been registered via @topic_handler. Exiting..."
                )
            )
            return

        self.stdout.write(self.style.SUCCESS("Registered topic handlers:"))
        for (topic, event), handler in REGISTERED_TOPIC_HANDLERS.items():
            self.stdout.write(f"- {topic} {event}: {handler.__name__}")

        consumer = Consumer(
            topics=REGISTERED_TOPICS,
            message_handlers=REGISTERED_TOPIC_HANDLERS,
            command=self,
        )

        consumer.begin_consume()
