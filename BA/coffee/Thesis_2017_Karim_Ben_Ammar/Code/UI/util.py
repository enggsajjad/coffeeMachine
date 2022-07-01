import sys
from urllib import request, error

def internet_on():
    try:
        request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except error.URLError as err:
        return False
