from src.dramatiq_tasks.utils import create_consumer
from src.dramatiq_tasks.tasks.example.queue import test_queue
from src.dramatiq_tasks.tasks.example.callback import example_callback


example_consumer = create_consumer(test_queue, example_callback)
