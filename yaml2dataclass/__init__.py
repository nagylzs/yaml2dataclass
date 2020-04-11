from typing import Optional, List, Union
import inspect

import yaml

SchemaPath = List[Union[str, int]]


class Schema:
    """Dataclass mixin that can load nested dataclasses."""

    @staticmethod
    def _str_load_path(path: SchemaPath):
        items = []
        for index, item in enumerate(path):
            if isinstance(item, int):
                items.append("[%d]" % index)
            else:
                items.append("." + item)
        return "".join(items)

    @classmethod
    def scm_load_yaml(cls, stream):
        """Load instance from stream."""
        return cls.scm_load_from_dict(yaml.safe_load(stream))

    @classmethod
    def scm_convert(cls, values: dict, path: SchemaPath):
        return values

    @classmethod
    def scm_load_from_dict(cls, values: dict, path: Optional[SchemaPath] = None):
        """Load instance from plain dictionary."""
        if path is None:
            path = []
            try:
                return cls.scm_load_from_dict(values, path)
            except TypeError as e:
                raise TypeError("%s%s: %s" % (cls.__name__, cls._str_load_path(path), e.args[0]))
        else:
            args = {}
            for name, value in cls.scm_convert(values, path).items():
                try:
                    typ = cls.__annotations__[name]
                except KeyError:
                    raise KeyError("Cannot set %s.%s - no such member." % (cls.__name__, name))
                if inspect.isclass(typ):
                    if issubclass(typ, Schema):
                        path.append(name)
                        args[name] = typ.scm_load_from_dict(value, path)
                        path.pop()
                    else:
                        args[name] = cls.scm_load_typ_from_dict(typ, name, value)
                else:
                    args[name] = value
            return cls(**args)

    @classmethod
    def scm_load_typ_from_dict(cls, typ, name, value):
        """Convert a value of a given type (for loading)."""
        return value

    @classmethod
    def scm_load_list_of_instances(cls, values: dict, name: str, path: Optional[SchemaPath] = None):
        if path is None:
            path = []
            try:
                return cls.scm_load_list_of_instances(values, name, path)
            except TypeError as e:
                raise TypeError("%s at %s: %s" % (cls.__name__, cls._str_load_path(path), e.args[0]))
        else:
            items = values.get(name, None)
            if items is None:
                return None
            if path is None:
                path = []
            path.append(name)
            result = []
            for index, value in enumerate(items):
                path.append(index)
                result.append(cls.scm_load_from_dict(value, path))
                path.pop()
            path.pop()
            return result
