from importlib import import_module
import os


MANUAL_TEST_DIR = 'acipenser/manual/'


def not_cache_file(file):
    return False if "__pycache" in file or ".pyc" in file else True


def get_file_name(file):
    try:
        file_name, extension = file.split('.')
    except ValueError:
        raise ValueError(
            "Error loading object '{}': not a full path".format(file))
        return False
    except:
        return False
    return file_name, extension


def is_py_file(extension):
    return True if extension == 'py' else False


def check_pattern(pattern, name):
    return True if pattern.replace('*', '') in name else False


def _get_class(module, path):
    _vars = dir(module)
    for _var in _vars:
        attr = getattr(module, _var)
        if not hasattr(attr, 'path'):
            continue
        value = getattr(attr, 'path')
        if value == path:
            return attr


def class_by_module_name(module_name, path):
    module = import_module(module_name)
    return _get_class(module, path)


def get_class_by_path(path, start_dir=MANUAL_TEST_DIR, pattern="test_"):
    files = os.listdir(start_dir)
    files = list(filter(not_cache_file, files))
    for file in files:
        file_name, extension = get_file_name(file)
        if not is_py_file(extension):
            continue
        if not check_pattern(pattern, file_name):
            continue
        module_name = (start_dir + file_name).replace('/', '.')
        module = import_module(module_name)
        cls = class_by_module_name(module_name, path)
        if cls:
            return cls


loader = get_class_by_path