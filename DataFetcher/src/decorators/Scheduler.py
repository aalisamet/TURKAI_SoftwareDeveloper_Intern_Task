import time

from configuration.ConfigDistributor import ConfigDistributorService


def blocking_scheduler(function):

    def wrapper(*args, **kwargs):

        interval = ConfigDistributorService().get_scheduler_config_data("scheduler", "interval")
        while True:
            function(*args, **kwargs)
            time.sleep(interval)
    return wrapper

