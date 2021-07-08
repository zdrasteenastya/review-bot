from typing import Mapping


def get_class_attributes(cls_with_attributes: type, public_only: bool = True) -> Mapping:
    """Get class attributes.

    :param cls_with_attributes: Class with attributes.
    :param public_only: A flag that prevents the display of protected class attributes.
    :return: Class attributes.
    """
    class_attributes = {}

    for attr_name, attr_value in getattr(cls_with_attributes, '__dict__', {}).items():
        if not public_only or not attr_name.startswith('_'):
            class_attributes[attr_name] = attr_value

    return class_attributes
