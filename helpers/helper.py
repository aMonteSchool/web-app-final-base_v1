from base.components.url import URL


def map_url(name: str):
    return getattr(URL, name.upper().replace('-', '_'))