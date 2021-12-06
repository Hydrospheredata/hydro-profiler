from profiler.utils.decode_url import decode_url


def test_decoded_url():
    original_url = "s3://foo.bar/inference/adult/batch_1.csv"
    encoded = "czM6Ly9mb28uYmFyL2luZmVyZW5jZS9hZHVsdC9iYXRjaF8xLmNzdg=="

    assert decode_url(encoded) == original_url
