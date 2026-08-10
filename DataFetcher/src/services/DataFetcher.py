
from selenium import webdriver
from .ConfigDistributer import ConfigDistributerService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions





class DataFetcherService:

    base_url=ConfigDistributerService().get_config_data("selenium","base_url")



    @staticmethod
    def create_driver():
        return webdriver.Chrome()


    def fetch_page_data_with_number(self,page_number:str):
        driver = self.create_driver()
        driver.minimize_window()
        wanted_list=[]
        search_value:str = ConfigDistributerService().get_config_data("search","search_value","list_item")
        try:
            driver.get(self.base_url+page_number)
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


    @staticmethod
    def get_wanted_person_information(wanted_person_url:str):
        driver = DataFetcherService.create_driver()
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

            print(f"İsim: {first_name} {last_name} | Cinsiyet: {gender} | Doğum Tarihi: {date_of_birth} | Doğum Yeri: {place_of_birth} | Milliyet: {nationality} ")
        except Exception as e:
            print(e)

        finally:
            driver.quit()
    def print_list(self):
        wanted_person_list = self.fetch_page_data_with_number("1")
        for wanted_person in wanted_person_list:
            DataFetcherService.get_wanted_person_information(wanted_person)
