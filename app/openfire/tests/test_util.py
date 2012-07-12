from openfire.core.sessions import SessionsMixin

'''
This module has utility functions used for the test suite.
'''

def encrypt(key):
    # TODO: Do this a better way?
    return SessionsMixin().encrypt(key)

def decrypt(key):
    # TODO: Do this a better way?
    return SessionsMixin().decrypt(key)

