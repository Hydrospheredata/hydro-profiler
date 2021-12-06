import base64


def decode_url(encoded_url: str) -> str:
    encoded_url_bytes = encoded_url.encode("ascii")
    decoded_url_bytes = base64.b64decode(encoded_url_bytes)
    return decoded_url_bytes.decode("ascii")
