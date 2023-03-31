import json
from src._taskiq.broker import broker
from src._taskiq.utils import create_producer
from src._taskiq.example.queue import test_queue


# Define a task that will be performed by the worker
@broker.task
def process_data(data):
    create_producer(test_queue)(json.dumps(data))
    print("Processing data, {}".format(data))
