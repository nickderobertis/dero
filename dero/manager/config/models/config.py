from typing import Callable, Any
import inspect

from dero.manager.config.logic.load.file import get_user_defined_dict_from_module, load_file_as_module
from dero.manager.config.logic.load.func import function_args_as_dict
from dero.manager.config.logic.write import dict_as_local_definitions_str
from dero.manager.pipelines.models.interfaces import PipelineOrFunction
from dero.manager.pipelines.models.pipeline import Pipeline

class Config(dict):

    def __init__(self, d: dict, name: str=None, **kwargs):
        super().__init__(d, **kwargs)
        self.name = name

    def __getattr__(self, attr):
        return self[attr]

    def __dir__(self):
        return self.keys()

    def update(self, d: dict, **kwargs):
        super().update(d, **kwargs)
        self._update_file_str()

    def to_file(self, filepath: str):
        with open(filepath, 'w') as f:
            f.write(self.file_str)

    @property
    def file_str(self):
        try:
            return self._file_str
        except AttributeError:
            self._file_str = dict_as_local_definitions_str(self)

        return self._file_str

    @classmethod
    def from_file(cls, filepath: str):
        module = load_file_as_module(filepath)
        config_dict = get_user_defined_dict_from_module(module)

        return cls(config_dict)

    @classmethod
    def from_function(cls, func: Callable):
        config_dict = function_args_as_dict(func)

        return cls(config_dict)

    def _update_file_str(self):
        # only update if already set
        if hasattr(self, '_file_str'):
            self._file_str = dict_as_local_definitions_str(self)

    @classmethod
    def from_pipeline(cls, item: PipelineOrFunction):
        init_func = _pipeline_class_or_instance_or_method_to_init_func(item)
        return cls.from_function(init_func)

    @classmethod
    def from_pipeline_or_function(cls, item: PipelineOrFunction):
        func = _function_or_pipeline_to_function(item)
        return cls.from_function(func)


def _function_or_pipeline_to_function(obj_or_class: Any) -> Callable:
    if _is_pipeline_instance_or_pipeline_class(obj_or_class) or _is_pipeline_method(obj_or_class):
        return _pipeline_class_or_instance_or_method_to_init_func(obj_or_class)

    # must be function separate from pipeline
    return obj_or_class

def _pipeline_class_or_instance_or_method_to_init_func(obj_or_class: Any) -> Callable:
    if _is_pipeline_instance_or_pipeline_class(obj_or_class):
        # Got Pipeline instance, or Pipeline class
        return obj_or_class.__init__
    if isinstance(obj_or_class, Callable):
        # Got method of pipeline class. Pull object, then pull init method
        return obj_or_class.__self__.__init__


def _is_pipeline_instance_or_pipeline_class(obj_or_class: Any) -> bool:
    return isinstance(obj_or_class, Pipeline) or (inspect.isclass(obj_or_class) and issubclass(obj_or_class, Pipeline))

def _is_pipeline_method(obj_or_class: Any) -> bool:
    if not _is_class_method(obj_or_class):
        return False

    # Must be a class method. Determine if is pipeline class
    obj = obj_or_class.__self__
    if isinstance(obj, Pipeline):
        return True

    return False

def _is_class_method(obj_or_class: Any) -> bool:
    if not isinstance(obj_or_class, Callable):
        # not a function, can't be a method
        return False

    if not hasattr(obj_or_class, '__self__'):
        # not a class method, standalone function
        return False

    return True