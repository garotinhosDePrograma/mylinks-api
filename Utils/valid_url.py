import re

def is_valid_url(url):
    pattern = re.compile(r'^https?://')
    return bool(pattern.match(url))
