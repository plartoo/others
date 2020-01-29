
class TransformFunctions(object):

    """
    ALL transform functions must be written as part of this class.
    getattr(obj, function_name)(*args, **kwargs)
    REF: https://stackoverflow.com/a/2203479
         https://stackoverflow.com/a/6322114
    """
    def _trim_space(cell_str):
        return str(cell_str).strip()


    def remove_dollars(data_row):
        pass


    def multiply_by_thousand():
        pass


    def rename_columns():
        # df.rename(columns=old_to_new_col_mappings, inplace=True) if not old_to_new_col_mappings
        pass
