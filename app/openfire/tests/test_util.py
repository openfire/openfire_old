from openfire.core.sessions import SessionsBridge

'''
This module has utility functions used for the test suite.
'''

def encrypt(key):
    # TODO: Do this a better way?
    return SessionsBridge().encrypt(key)

def decrypt(key):
    # TODO: Do this a better way?
    return SessionsBridge().decrypt(key)

