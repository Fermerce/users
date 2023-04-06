from src.taskiq.utils import create_consumer
from src.taskiq.example.queue import test_queue
from src.taskiq.example.callback import example_callback


example_consumer = create_consumer(test_queue, example_callback)
