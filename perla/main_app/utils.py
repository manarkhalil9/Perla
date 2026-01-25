import random
from .quotes_data import POSITIVE_QUOTES

def get_quote():
    data = random.choice(POSITIVE_QUOTES)
    return data