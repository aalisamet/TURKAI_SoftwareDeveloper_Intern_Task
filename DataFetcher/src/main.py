from decorators.Scheduler import blocking_scheduler
from services.HttpDataFetcher import HttpDataFetcherService
from messaging.RabbitMQPublisher import MQPublisher



@blocking_scheduler
def den():

    people = HttpDataFetcherService.request_wanted_profiles()
    MQPublisher.publish_all_list_in_single_connection(people)




if __name__ == '__main__':

    den()