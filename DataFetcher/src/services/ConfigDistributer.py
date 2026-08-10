import pathlib
import yaml
class ConfigDistributerService:

    def __init__(self):
        self.path = pathlib.Path(__file__).parent.absolute().parent.absolute().parent.absolute().joinpath('config/DataProviderConfig.yaml')
        try:
            with open(self.path, 'r') as file:
                self.config_data = yaml.safe_load(file)
        except FileNotFoundError:
            print("Config file not found.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
        finally:
            file.close()

    def get_config_data(self,*args):
        data = self.config_data
        for argument in args:
            data = data[argument]
        return data

