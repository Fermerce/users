import sys
import time
import dramatiq
from src.dramatiq_tasks._repository import consumer_list
from src.dramatiq_tasks.config import connection
from src.dramatiq_tasks.utils import discover
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from src.lib.base.settings import config

# Set up the broker
broker = RabbitmqBroker(url=config.get_broker_url(include_virtue=False))
dramatiq.set_broker(broker)

actors = discover("./src/dramatiq_tasks/tasks")

worker = dramatiq.Worker(broker=broker, worker_timeout=10000)
worker.start()


def run():
    while True:
        try:
            for consumer in consumer_list:
                consumer()
            time.sleep(1)
        except connection.connection_errors:
            print("connection revived")
        except KeyboardInterrupt:
            print("Stopping consumer thread")
            sys.exit(1)


if __name__ == "__main__":
    run()
