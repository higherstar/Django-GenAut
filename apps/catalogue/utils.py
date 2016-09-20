from itertools import cycle, izip
import base64


key = '25SSSscfWoen4deRPNGbKo5jnnpQ6pxGKWG5eZojZFvzX2rcok'


def encrypt(message):
    return base64.urlsafe_b64encode(''.join(chr(ord(c)^ord(k)) for c,k in izip(message, cycle(key))))

def decrypt(message):
    return ''.join(chr(ord(c)^ord(k)) for c,k in izip(base64.urlsafe_b64decode(message), cycle(key)))