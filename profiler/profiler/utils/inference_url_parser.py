from urllib.parse import urlparse


def extract_file_name(url: str):
    parsed = urlparse(url)
    return parsed.path.split("/")[-1]
