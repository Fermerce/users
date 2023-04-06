from kombu import Queue
from src.taskiq.config import exchange


test_queue = Queue(
    name="tasks",
    exchange=exchange,
    routing_key="tasks",
)
