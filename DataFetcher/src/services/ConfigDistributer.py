import pathlib
import yaml

class ConfigDistributerService:

    def __init__(self):
        path = pathlib.Path(__file__).parent.absolute().parent.absolute().parent.absolute().joinpath('config/DataProviderConfig.yaml')
        try:
            with open(path, 'r') as file:
                self.provider_config_data = yaml.safe_load(file)
        except FileNotFoundError:
            print("Config file not found.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
        finally:
            file.close()

        path = pathlib.Path(__file__).parent.absolute().parent.absolute().parent.absolute().joinpath(
            'config/SchedulerConfig.yaml')
        try:
            with open(path, 'r') as file:
                self.scheduler_config_data = yaml.safe_load(file)
        except FileNotFoundError:
            print("Config file not found.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
        finally:
            file.close()








    @staticmethod
    def get_provider_config_data(*args):
        data = ConfigDistributerService().provider_config_data
        for argument in args:
            data = data[argument]
        return data

    @staticmethod
    def get_scheduler_config_data(*args):
        data = ConfigDistributerService().scheduler_config_data
        for argument in args:
            data = data[argument]
        return data