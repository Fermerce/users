import sys
import time
from src.taskiq._repository import consumer_list
from src.taskiq.config import connection
from src._base.settings import config
from taskiq_aio_pika import AioPikaBroker


# Set up the broker
broker = AioPikaBroker(
    url=config.get_broker_url(),
    exchange_name=config.project_name.lower() if config.project_name else "taskiq",
)


# from src.dramatiq_tasks.utils import discover


def run():
    while True:
        try:
            for consumer in consumer_list:
                consumer()
        except connection.connection_errors:
            print("connection revived")
            time.sleep(2)
        except KeyboardInterrupt:
            print("Stopping consumer thread")
            sys.exit(1)


if __name__ == "__main__":
    run()
