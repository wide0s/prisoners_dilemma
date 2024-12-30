from players import BasePlayer
from players import EXCLUDE_PLAYERS


class ClassNotFoundError(ValueError):
    pass


class PlayerFactory:
    @staticmethod
    def get(class_name: str) -> object:
        assert type(class_name) == str, "class_name must be a string!"
        if class_name in EXCLUDE_PLAYERS:
            raise ClassNotFoundError(class_name)
        def enum_subclasses(clazz, subclasses=None):
            if subclasses == None:
                subclasses = []
            clazz_subclasses = clazz.__subclasses__()
            if len(clazz_subclasses) == 0:
                return subclasses
            subclasses += clazz_subclasses
            for subclazz in clazz_subclasses:
                enum_subclasses(subclazz, subclasses)
            return subclasses
        raw_subclasses_ = enum_subclasses(BasePlayer)
        classes: dict[str, Callable[..., object]] = {c.__name__:c for c in raw_subclasses_}
        class_ = classes.get(class_name, None)
        if class_ is not None:
            return class_

        raise ClassNotFoundError


    @staticmethod
    def class_names() -> list:
        def enum_class_names(clazz, clazz_names=None):
            if clazz_names == None:
                clazz_names = []
            clazz_subclasses = clazz.__subclasses__()
            if len(clazz_subclasses) == 0:
                return clazz_names
            for subclazz in clazz_subclasses:
                # FIX: enumerate all subclasses and exclude after enumeration,
                # currently this logic excludes sub classes :(
                if subclazz.__name__ in EXCLUDE_PLAYERS:
                    continue
                clazz_names.append(subclazz.__name__)
                enum_class_names(subclazz, clazz_names)
            return clazz_names
        return sorted(enum_class_names(BasePlayer))
