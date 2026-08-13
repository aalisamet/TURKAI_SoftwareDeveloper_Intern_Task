import yaml
import pathlib

class ConfigDistributorService:


    def __init__(self):

        def open_config_file(config_file_name):
            path = pathlib.Path(__file__).parent.absolute().parent.absolute().parent.absolute().joinpath(
                f'config/{config_file_name}')
            try:
                with open(path, 'r') as file:
                    return yaml.safe_load(file)
            except FileNotFoundError:
                print("Config file not found.")
            except yaml.YAMLError as e:
                print(f"Error parsing YAML: {e}")
            finally:
                file.close()

        self.rabbitmq_config_data = open_config_file('RabbitMQConfig.yaml')







    @staticmethod
    def get_rabbitmq_config_data(*args):
        data = ConfigDistributorService().rabbitmq_config_data
        for argument in args:
            data = data[argument]
        if data is None:
            print("Config file corrupted.")
            return ""
        return data

