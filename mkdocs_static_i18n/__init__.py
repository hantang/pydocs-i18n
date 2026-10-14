from pathlib import PurePath

version = "1.3.3"


def is_relative_to(src_path, dest_path):
    return PurePath(src_path).is_relative_to(dest_path)
