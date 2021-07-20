import io


def to_file_stream(file_bytes: bytes):
    return io.StringIO(file_bytes.decode("UTF8"))
