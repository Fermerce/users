from src._taskiq.utils import create_consumer
from src._taskiq.example.queue import test_queue
from src._taskiq.example.callback import example_callback


example_consumer = create_consumer(test_queue, example_callback)
