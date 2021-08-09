def split_in_chunks(lst: list, chunk_capacity: int = 10):
    for i in range(0, len(lst), chunk_capacity):
        yield lst[i : i + chunk_capacity]
