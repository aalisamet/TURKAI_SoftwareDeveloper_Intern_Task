import asyncio

from src.decorators.Scheduler import blocking_scheduler
from src.services.HttpDataFetcher import HttpDataFetcherService


if __name__ == '__main__':
    people = asyncio.run(HttpDataFetcherService.request_wanted_profiles())
    for person in people:
        print(person)

