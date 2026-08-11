from selenium import webdriver
from .ConfigDistributer import ConfigDistributerService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from src.models.WantedPerson import WantedPerson

'''
Cok onemli " https://ws-public.interpol.int/notices/v1/red?resultPerPage=100&page=1 "
ile ilk 100 aranan kisi dogrudan json olarak cekilebilir iohttp ile bu datalar


'''


class SeleniumDataFetcherService:

    base_url=ConfigDistributerService().get_provider_config_data("selenium", "base_url")

    #brings a driver instance
    @staticmethod
    def create_driver():


        #chrome_options = Options()
        #chrome_options.add_argument("--headless=new")
        #chrome_options.page_load_strategy="normal"
        #chrome_options.add_argument("--window-size=1920,1080")
        #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        return webdriver.Chrome()

    @staticmethod
    #Collecting wanted person profile urls
    def fetch_page_data_with_number(page_number:str):

        driver = SeleniumDataFetcherService.create_driver()
        driver.minimize_window()
        wanted_list=[]
        search_value:str = ConfigDistributerService().get_provider_config_data("search", "search_value", "list_item")
        try:
            driver.get(SeleniumDataFetcherService.base_url + page_number)
            wait = WebDriverWait(driver, 10)
            items = wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, search_value)))

            for item in items:
                my_url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                wanted_list.append(my_url)

        except Exception as e:
            print(e)

        finally:
            driver.quit()
        return wanted_list



    #Collecting Wanted Person info
    @staticmethod
    def get_wanted_person_information(wanted_person_url:str) -> WantedPerson:
        driver = SeleniumDataFetcherService.create_driver()
        try:
            driver.get(wanted_person_url)
            driver.minimize_window()
            wait = WebDriverWait(driver, 10)
            item = wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "tbody")))

            first_name = item.find_element(By.ID, "forename").text.strip()
            last_name = item.find_element(By.ID, "name").text.strip()
            gender = item.find_element(By.ID, "sex_id").text.strip()
            date_of_birth = item.find_element(By.ID, "date_of_birth").text.strip()
            place_of_birth = item.find_element(By.ID, "place_of_birth").text.strip() + item.find_element(By.ID, "country_of_birth_id").text.strip()
            nationality = item.find_element(By.ID, "nationalities").text.strip()

            wanted_person = WantedPerson(first_name=first_name, last_name=last_name, gender=gender, date_of_birth=date_of_birth, place_of_birth=place_of_birth, nationality=nationality)

            return wanted_person
        except Exception as e:
            print(e)
            return WantedPerson.no_args_constructor()
        finally:

            driver.quit()


    @staticmethod
    #Test Func
    def print_list():
        wanted_person_links = SeleniumDataFetcherService.fetch_page_data_with_number("1")
        wanted_person_list = []
        for wanted_person_link in wanted_person_links:
            wanted_person = SeleniumDataFetcherService.get_wanted_person_information(wanted_person_link)
            wanted_person_list.append(wanted_person)


        for wanted_person in wanted_person_list:
            print(wanted_person)
        return wanted_person_list
