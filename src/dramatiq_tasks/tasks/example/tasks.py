import json
import dramatiq
from src.dramatiq_tasks.utils import create_producer
from src.dramatiq_tasks.tasks.example.queue import test_queue


# Define a task that will be performed by the worker
@dramatiq.actor
def process_data(data):
    create_producer(test_queue)(json.dumps(data))
    print("Processing data, {}".format(data))
