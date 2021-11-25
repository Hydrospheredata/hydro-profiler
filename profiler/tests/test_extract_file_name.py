from profiler.utils.inference_url_parser import extract_file_name


def test_extract_file_name():
    url = "s3://ecommerce-basic/inference/ecommerce_products_0-500.csv"

    assert extract_file_name(url) == "ecommerce_products_0-500.csv"
