def get_file_data(path: str, raise_on_empty: bool = True):
    with open(path) as f:
        data = [line.rstrip() for line in f]

        if raise_on_empty and not len(data):
            raise Exception(f"{path} is empty")

        return data
