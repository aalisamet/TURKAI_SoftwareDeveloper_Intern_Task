import aiohttp
import asyncio
import requests
from configuration.ConfigDistributor import ConfigDistributorService
from models.WantedPerson import WantedPerson


class HttpDataFetcherService:
    __base_url = ConfigDistributorService.get_provider_config_data("http", "base_url")
    __number_of_results = ConfigDistributorService.get_provider_config_data("http", "number_of_results")
    __request_header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Host": "ws-public.interpol.int",
        "Priority": "u=0, i",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0"
    }




    @staticmethod
    def __request_wanted_links():
        try:
            if int(HttpDataFetcherService.__number_of_results)>160 or int(HttpDataFetcherService.__number_of_results)<1:
                HttpDataFetcherService.__number_of_results = 160
        except ValueError:
            HttpDataFetcherService.__number_of_results = 159
        try:
            wanted_people_response = requests.get(HttpDataFetcherService.__base_url + HttpDataFetcherService.__number_of_results, headers=HttpDataFetcherService.__request_header).json()
        except requests.RequestException as e:
            print(f"Error fetching wanted people data: {e}")
            wanted_people_response = {"_embedded": {"notices": []}}
        print(wanted_people_response)
        wanted_profile_list= [x["_links"]["self"]["href"] for x in wanted_people_response["_embedded"]["notices"]]
        #print(wanted_profile_list)
        return wanted_profile_list

    @staticmethod
    def create_wanted_profile_with_json(response):
        first_name = response["name"]
        last_name = response["forename"]
        gender = response["sex_id"]
        date_of_birth = response["date_of_birth"]
        place_of_birth = response["place_of_birth"]
        nationality = response["nationalities"]
        height = response["height"]
        wanted_person = WantedPerson(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            place_of_birth=place_of_birth,
            nationality=nationality,
            height=height)

        return wanted_person

    @staticmethod
    async def request_wanted_profiles_async():
        urls = HttpDataFetcherService.__request_wanted_links()
        async def fetch(session, url):
            async with session.get(url) as response:
                profile_response = await response.json()
                wanted_person = HttpDataFetcherService.create_wanted_profile_with_json(profile_response)
                await asyncio.sleep(1)  # Simulate some processing time
                return wanted_person

        wanted_list =[]
        async with asyncio.Semaphore(2):
            async with (
                aiohttp.ClientSession(headers=HttpDataFetcherService.__request_header) as session):
                tasks = [fetch(session, url) for url in urls]
                wanted_list.extend(await asyncio.gather(*tasks))

            return wanted_list

    @staticmethod
    def request_wanted_profiles():

        urls = HttpDataFetcherService.__request_wanted_links()
        wanted_list = []

        for url in urls:
            profile_response = requests.get(url,headers=HttpDataFetcherService.__request_header).json()
            wanted_list.append(HttpDataFetcherService.create_wanted_profile_with_json(profile_response))
        return wanted_list


# abilities = [x["ability"]["name"] for x in data["abilities"]]

'''
import requests
from threading import Thread
import time
import aiohttp
import asyncio

urls = ["https://postman-echo.com/delay/2"]*5


#

def request_sync():

    start_time = time.time()
    json_list = []

    for url in urls:
        response = requests.get(url).json()
        json_list.append(response)



    end_time = time.time()
    print(f"Total time taken: {end_time - start_time}")

def request_async():
    start_time = time.time()
    json_list = []

    threads = []
    for url in urls:
        thread = Thread(target=lambda: json_list.append(requests.get(url).json()))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time}")



async def request_asyncio():
    st = time.time()

    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.json()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        json_list = await asyncio.gather(*tasks)

    et = time.time()
    print(f"Total time taken: {et-st}")
    return json_list
if __name__ == "__main__":
    asyncio.run(request_asyncio())

'''