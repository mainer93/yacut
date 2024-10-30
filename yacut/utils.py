import random
import string

from .settings import Constants


def get_unique_short_id(length=Constants.MAX_LENGTH):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
