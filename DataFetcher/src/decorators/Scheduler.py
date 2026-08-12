import time

from services.ConfigDistributer import ConfigDistributerService


def blocking_scheduler(function):

    def wrapper(*args, **kwargs):

        interval = ConfigDistributerService().get_scheduler_config_data("scheduler", "interval")
        while True:
            function(*args, **kwargs)
            time.sleep(interval)
    return wrapper

