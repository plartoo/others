import transform_errors

if __name__ == '__main__':
    raise transform_errors.RedundantJSONKeyError('key1','key2')
    # raise transform_errors.FileNotFound('test_file')
