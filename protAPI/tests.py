from django.test import TestCase

# Create your tests here.

def init(*args):
    if 'staleonly' in args:
        print("Todo ok", args)


