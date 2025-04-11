import random
import string

def generate_key(number):

    """
    This is a comenter about this function, whose only purpose is generate random number and make nothing more for you
    """
    caracteres = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=number))
    return caracteres
    
if __name__ == '__main__':
    pass