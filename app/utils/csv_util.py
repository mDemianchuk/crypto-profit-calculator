import csv
import io


def read_csv(file_bytes: bytes):
    file_stream = io.StringIO(file_bytes.decode("UTF8"))
    return list(csv.DictReader(file_stream))
