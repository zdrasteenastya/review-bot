import inspect
import json
from typing import Callable, Mapping

from helpers.misc import get_class_attributes


class SettingsReader(object):
    def __init__(self, settings_module):
        """Read application settings from config classes."""
        self.settings_module = settings_module

    def get_settings(self, public_only: bool = True) -> Mapping:
        """Get application settings.

        :param public_only: A flag that prevents the display of protected class attributes.
        :return: Application settings.
        """
        app_settings = {}
        for config_name, config_cls in inspect.getmembers(self.settings_module):
            if inspect.isclass(config_cls):
                app_settings[config_name] = get_class_attributes(config_cls, public_only=public_only)

        return app_settings

    def print_settings(self, print_func: Callable = print, public_only: bool = True) -> None:
        """Print application settings into console.

        :param print_func: Function for printing settings.
        :param public_only: A flag that prevents the display of protected class attributes.
        """
        for config_name, config_attributes in self.get_settings(public_only).items():
            print_func(f'{config_name}:\n')
            for param_name, param_value in config_attributes.items():
                if isinstance(param_value, dict):
                    param_value = json.dumps(param_value, default=str, indent=4)
                print_func(f'{param_name} = {param_value}')
            print_func('\n')
