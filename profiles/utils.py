from urllib.parse import urlparse


def get_hostname_from_url(url) -> str:
    # Get hostname from url
    hostname = urlparse(url).hostname

    # Remove the www. prefix, if present.
    if hostname.startswith("www."):
        hostname = hostname[4:]

    # Split the hostname by the dot.
    domain_parts = hostname.split(".")

    # The second level domain is the first part of the domain.
    return domain_parts[0]
