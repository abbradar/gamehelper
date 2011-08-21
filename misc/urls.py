from django.conf import settings
from re import escape

def abs_regex(regex):
    if settings.ROOT_URL == '':
        return regex
    else:
        abs = r'^' + escape(settings.ROOT_URL[1:])
        if not regex.startswith('^'):
            abs = abs + r'.*'
        else:
            regex = regex[1:]
        return abs + regex

def abs_url(path):
    if path.startswith('/') and settings.ROOT_URL != '':
        path = settings.ROOT_URL + path[1:]
    return path
