import importlib
import json
import pathlib

from constants.transform_constants import *
import transform_errors


def load_config(config_file):
    """
    Loads the config file as JSON.
    REF: https://web.archive.org/web/20181002170353/https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
    """
    with open(config_file, 'r') as f:
        return json.load(f)


def insert_input_file_keys_values_to_config_json(file_path_and_name, config):
    """
    Inserts input file's path and name as values to corresponding keys
    in config JSON. This method is called if user provides input file
    path and name info via commandline instead of via config file.

    This is more like a hack because feeding input file information via
    commandline is an afterthought (originally, I was not very keen on it,
    but then I realized if we are to use one common config file to do,
    for example, QA-testing of common patterns, this commandline feeding
    of input file name can be much neater than creating similar config
    file one per country.
    """
    config[KEY_INPUT_FOLDER_PATH] = os.path.split(file_path_and_name)[0]
    config[KEY_INPUT_FILE_NAME_OR_PATTERN] = os.path.split(file_path_and_name)[1]
    return config


def _assert_required_keys(config):
    """Checks if all required keys exist in the config loaded."""
    for k in REQUIRED_KEYS:
        if k not in config:
            raise transform_errors.RequiredKeyNotFoundInConfigFile(k)


def _assert_expected_data_types(config):
    """Checks if loaded config has values that are of expected data types."""
    for k, types in EXPECTED_CONFIG_VALUE_DATA_TYPES.items():
        # We use 'any' because we want to allow some of the keys
        # to be, for example, either int or None, and
        # EXPECTED_CONFIG_DATA_TYPES can be configured with
        # something like {KEY_NAME : [int, None]}
        # print(k, "=>", config[k], "=>", types)
        if (k in config) and (not any([isinstance(config[k], t) for t in types])):
            raise transform_errors.ConfigFileInputDataTypeError(k, types)


def validate_configurations(config):
    """Calls other helper functions to check on the validity of config JSON"""
    _assert_required_keys(config)
    _assert_expected_data_types(config)


def get_input_files(config):
    """
    Returns the input file(s) based on the file name/pattern
    in the input folder name provided in the JSON config file.
    """
    fn = os.path.join(config[KEY_INPUT_FOLDER_PATH],
                      config[KEY_INPUT_FILE_NAME_OR_PATTERN])
    # REF: https://stackoverflow.com/a/41447012/1330974
    input_files = [str(f.absolute()) for f in pathlib.Path().glob(fn)]

    if not input_files:
        raise transform_errors.FileNotFound(fn)
    return input_files


def get_write_data_decision(config):
    """
    Get boolean value that tells the program whether to
    write the output (transformed dataframe) to somewhere.
    """
    return config.get(KEY_WRITE_OUTPUT,
                      DEFAULT_WRITE_OUTPUT)


def _get_classes_defined_in_module(python_module):
    # REF: https://stackoverflow.com/a/61471777/1330974
    return [v for k, v in vars(python_module).items() if isinstance(v, type)]


def _extract_possible_primary_class_name_from_module_name(abs_or_rel_module_name):
    """
    Given a Python module name (be it in absolute terms like
    'data_writers.excel_data_writer' or in relative terms like
    '.excel_data_writer' or just 'excel_data_writer'),
    this method will extract the real module in this name
    (in the above example, it is 'excel_data_writer'),
    lowercase it and return it as the possible primary class
    name.

    Note: This assume that the programmer who wrote
    the module named the Python module file and the
    class names to be the same (ignoring the underscores)
    based on the widely-accepted Python naming convention.
    """
    last_module_name = abs_or_rel_module_name.split('.')[-1]
    return ''.join([w.lower() for w in last_module_name.split('_')])


def _get_primary_class_from_module(python_module):
    """
    Given a Python module, try to predict its main/primary
    class from the module by lowercase string matching, and
    return it.

    The underlying assumption made in this method that
    the programmer gave module and class names according
    to Python's standard naming convention (i.e. CamelCase
    for class names and underscore for module_or_file_names).
    """
    klasses = _get_classes_defined_in_module(python_module)
    possible_primary_kls_name = _extract_possible_primary_class_name_from_module_name(
        python_module.__name__)

    return [kls for kls in klasses
            if kls.__name__.lower() == possible_primary_kls_name][0]


def _get_module_name_in_absolute_term(module_file_path_and_name):
    # Using relpath sanitize module file path and name (regardless of
    # whether the input parameter is an absolute or relative path)
    # into something like 'data_writers/excel_data_writer.py',
    # which makes it easier to transform that into parameter for
    # import_module function.
    rel_path_and_file_name = os.path.relpath(module_file_path_and_name)
    # Then, we remove the file extension like below and are left with
    # something like: 'data_writers/excel_data_writer'
    rel_path_and_file_name_without_file_ext = os.path.splitext(
        rel_path_and_file_name)[0]
    return rel_path_and_file_name_without_file_ext.replace(os.sep, '.')


def instantiate_class_in_module_file(module_file_path_and_name):
    """
    This method will return the class with the matching
    name in the module file. For example, if the module file
    is 'excel_data_writer.py', this method will try to
    import the module and return ExcelDataWriter class
    in that module file.
    """
    if os.path.isfile(module_file_path_and_name):
        # Suppose the module file is:
        # C://Users/lachee/data_transformer/reader_writers/data_writers/excel_writer.py
        # we can use import_module in the two ways as below
        # importlib.import_module('reader_writers.data_writers.excel_writer')
        # or
        # importlib.import_module('.excel_writer', package='reader_writers.data_writers')
        # REF1: https://stackoverflow.com/a/10675081/1330974
        # REF2: https://stackoverflow.com/a/8899345/1330974
        # I decided to go with my personal preference below,
        # by using the first method signature.
        module = importlib.import_module(
            _get_module_name_in_absolute_term(module_file_path_and_name))

        return _get_primary_class_from_module(module)
    else:
        raise transform_errors.FileNotFound(module_file_path_and_name)


def instantiate_data_writer_class(config):
    data_writer_module_file = config.get(
        KEY_DATA_WRITER_MODULE_FILE,
        DEFAULT_DATA_WRITER_MODULE_FILE)
    return instantiate_class_in_module_file(data_writer_module_file)(config)


def instantiate_transform_functions_class(config):
    transform_funcs_module_file = config.get(
        KEY_CUSTOM_TRANSFORM_FUNCTIONS_FILE,
        DEFAULT_COMMON_TRANSFORM_FUNCTIONS_FILE)
    return instantiate_class_in_module_file(transform_funcs_module_file)()


def _is_any_key_in_dict(dictionary, list_of_keys):
    """
    Checks to see if any of the keys in 'list_of_keys' is present
    in the dictionary. Returns True if at least one keys in the list
    exists in the dictionary. Otherwise, returns False.

    Args:
        dictionary: Dictionary to inspect the keys.
        list_of_keys:   List of keys (e.g., ['key1','key2']) that should be
                        present in the dictionary.

    Returns:
        True or False depending on if any of the key(s) exist in the dictionary.
    """
    return any(k in dictionary for k in list_of_keys)


def get_functions_to_apply(config):
    """
    Returns the list of dicts where each dict follows structure like
    below to embed each transform/assert function and its parameters:
    [
        {
            "transform_function_name": "drop_columns",
            "transform_function_args, [[1,2,3]],
            "transform_function_kwargs, {"key1":"val1", "key2":"val2"},
        },
        {
            "assert_function_name": "drop_columns",
            "assert_function_args, [[1,2,3]],
            "assert_function_kwargs, {"key1":"val1", "key2":"val2"},
        },
    ]
    """
    funcs_list = config.get(KEY_FUNCTIONS_TO_APPLY,
                            list())

    if not funcs_list:
        # Function list must NOT be empty
        raise transform_errors.ListEmptyError(KEY_FUNCTIONS_TO_APPLY)

    for func_and_var in funcs_list:
        if type(func_and_var) is not dict:
            # Function and their corresponding parameters should be wrapped
            # in a dictionary as described in the documentation above.
            # E.g., [{"transform_function_name": "func_1", "transform_function_args": [[12]]}, ...]
            raise transform_errors.ConfigFileInputDataTypeError(KEY_FUNCTIONS_TO_APPLY, [dict])

    return funcs_list


def get_function_name(dict_of_func_and_params):
    """
    Extract and return function name (string type) from the dictionary
    that holds the function name and parameters (args/kwargs), if any.

    Args:
        dict_of_func_and_params: Dictionary that has function name and
        parameters like this:
          {
            "__function_comment__": "Drop empty columns in Budget roll up Excel file.",
            "function_name": "drop_unnamed_columns",
            "function_args": [["Unnamed 1", "Unnamed 2"]]
          }

    Returns:
         Function name (string) that we will convert to class attribute and invoke
         for data transformation.

    Raises:
        RequiredKeyNotFound: Return this error if there is no expected function key
        in the dictionary.
    """
    if not _is_any_key_in_dict(dict_of_func_and_params, [KEY_FUNC_NAME]):
        # This means the user did not not provide function name
        # for us to apply in the transform process
        raise transform_errors.RequiredKeyNotFound(dict_of_func_and_params,
                                                   [KEY_FUNC_NAME])

    return dict_of_func_and_params.get(KEY_FUNC_NAME, None)


def get_function_args(dict_of_func_and_params):
    """
    Extract and return list of arguments (*args) or an empty
    list from the dictionary that holds function name and
    parameters (args and kwargs), if any.

    Args:
        dict_of_func_and_params: Dictionary that has function name and
        parameters like this:
          {
            "__function_comment__": "Drop empty columns in Budget roll up Excel file.",
            "function_name": "drop_unnamed_columns",
            "function_args": [["Unnamed 1", "Unnamed 2"]]
          }

    Returns:
         List of parameters like [param1, param2] or an empty list if
         "function_args" key does not exists in the dictionary.
    """
    return dict_of_func_and_params.get(KEY_FUNC_ARGS, list())


def get_function_kwargs(dict_of_func_and_params):
    """
    Extract and return list of keyword arguments (*kwargs) or an empty list
    from the dictionary that holds function name and parameters
    (args and kwargs), if any.

    Args:
        dict_of_func_and_params: Dictionary that has function name and
        parameters like this:
          {
            "__function_comment__": "Drop empty columns in Budget roll up Excel file.",
            "function_name": "map_channel_columns",
            "function_kwargs": {"Amazon": "E-Commerce", "Ecommerce": "E-Commerce"}
          }

    Returns:
         Dictionary of keyword parameters like {"col1": "mapped_col_1", "col2": "mapped_col_2"}
         or an empty dictionary if "function_kwargs" key does not exist in the dictionary.
    """
    return dict_of_func_and_params.get(KEY_FUNC_KWARGS, dict())
