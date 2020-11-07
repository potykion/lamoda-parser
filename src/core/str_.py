import uuid


def random_file_name(extension: str = "jpg") -> str:
    """
    >>> random_file_name("png").endswith(".png")
    True
    """
    file_name = str(uuid.uuid4().hex)
    return f"{file_name}.{extension}"


