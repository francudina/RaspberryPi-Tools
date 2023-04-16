import json


def read_file(file_path: str, raise_exception: bool = True):
    try:
        with open(file_path, 'r', encoding="utf-8") as fh:
            return json.loads(fh.read())
    except Exception as e:
        if raise_exception:
            raise e
        return None
