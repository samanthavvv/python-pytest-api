from utils.format_data_tool.models import Config
from utils.path_tool.set_path import ensure_path_sep
from utils.yaml_tool.yaml_control import GetYamlData

_data = GetYamlData(ensure_path_sep("\common\config.yaml")).get_yaml_data()
config = Config(**_data)

if __name__ == '__main__':
    print(config)