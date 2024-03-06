from events.types import TopicKey


class TopicContextFilter:
    def __init__(self):
        self.topic = None
        self.event = None
        self.version = None
        self.func = None

    def set_context(self, key: TopicKey, func):
        self.topic = key.topic
        self.event = key.event
        self.version = key.version
        self.func = func

    def clear_context(self):
        self.topic = None
        self.event = None
        self.version = None
        self.func = None

    def filter(self, record):
        record.topic = self.topic or "N/A"
        record.event = self.event or "N/A"
        record.version = self.version or "N/A"
        record.func = self.func or "N/A"
        return True


topic_filter = TopicContextFilter()
