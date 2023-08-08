from urllib.parse import urlparse

from django.utils.safestring import mark_safe


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


def create_html_image(image):
    return mark_safe(
        f"""
            <a href='{image.url}'><img src="{image.url}" style="height:400px; width: 600px; border: 2px gray #333; 
                padding: 6px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);"> 
            </a>
        """
    )
