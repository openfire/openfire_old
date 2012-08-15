# -*- coding: utf-8 -*-
"""
Encryption/decryption tests.
"""

import unittest

from google.appengine.ext import ndb
from openfire.tests import OFTestCase

AES = None
try:
    from Crypto.Cipher import AES
except:
    pass

class BasicEncryptTestCase(OFTestCase):

    ''' Tests basic b64 obfuscation. '''

    def test_basic_encryption(self):

        # prepare cleartext
        simple_cleartext = "hello this is a test of the basic encryption mechanism"

        # encrypt and decrypt
        encrypted_text = self.encrypt(simple_cleartext, simple=True, cipher=False)
        self.assertTrue(encrypted_text, 'Simple encryption failed to encrypt a cleartext string.')

    def test_basic_encryption_decryption(self):

        # prepare cleartext
        simple_cleartext = "hello this is a test of the basic encryption mechanism"

        # encrypt and decrypt
        encrypted_text = self.encrypt(simple_cleartext, simple=True, cipher=False)
        decrypted_text = self.decrypt(encrypted_text)

        self.assertTrue(encrypted_text, 'Simple encryption failed to encrypt a cleartext string.')
        self.assertTrue(decrypted_text, 'Simple encryption failed to decrypt a ciphertext string.')
        self.assertEqual(simple_cleartext, decrypted_text, 'Simple encryption failed to properly encrypt or decrypt, because the resulting cleartext after decryption does not match the original.')

    def test_basic_key_encryption_decryption(self):

        # prepare key
        key_original = ndb.Key('TestKind', 'sample_keyname', parent=ndb.Key('TestParent', 1234))
        key_cleartext = key_original.urlsafe()

        # encrypt and decrypt
        encrypted_key = self.encrypt(key_cleartext, simple=True, cipher=False)
        decrypted_key = self.decrypt(encrypted_key)

        try:
            key_reconstructed = ndb.Key(urlsafe=decrypted_key)
        except Exception:
            key_reconstructed = False

        self.assertEqual(key_cleartext, decrypted_key, 'Simple encryption failed to properly encrypt or decrypt the key, because the resulting cleartext key after decryption does not match the original cleartext key.')

        self.assertTrue(key_reconstructed, 'Could not build key object from decoded cleartext key. Simple encryption probably mangled it.')
        self.assertEqual(key_original, key_reconstructed, 'The resulting encrypted+decrypted key does not match the original key object.')


class AdvancedEncryptTestCase(OFTestCase):

    ''' Tests AES-based encryption. '''

    @unittest.expectedFailure
    def test_aes_support(self):

        # Try to import AES
        self.assertTrue(AES, 'Could not load PyCrypt AES support. All advanced encryption tests will fail.')

    def test_advanced_encryption(self):

        # prepare cleartext
        advanced_cleartext = "hello this is a test of the advanced encryption mechanism"

        # encrypt and decrypt
        encrypted_text = self.encrypt(advanced_cleartext, simple=False, cipher=True)
        decrypted_text = self.decrypt(encrypted_text)

        self.assertEqual(advanced_cleartext, decrypted_text, 'Advanced encryption failed to properly encrypt or decrypt, because the resulting cleartext does not match.')

    def test_advanced_key_encryption(self):

        # prepare key
        key_original = ndb.Key('TestKind', 'sample_keyname', parent=ndb.Key('TestParent', 1234))
        key_cleartext = key_original.urlsafe()

        # encrypt and decrypt
        encrypted_key = self.encrypt(key_cleartext, simple=False, cipher=True)
        decrypted_key = self.decrypt(encrypted_key)

        try:
            key_reconstructed = ndb.Key(urlsafe=decrypted_key)
        except Exception:
            key_reconstructed = False

        self.assertEqual(key_cleartext, decrypted_key, 'Advanced encryption failed to properly encrypt or decrypt the key, because the resulting cleartext key does not match.')

        self.assertTrue(key_reconstructed, 'Could not build key object from decoded cleartext key. Advanced encryption probably mangled it.')
        self.assertEqual(key_original, key_reconstructed, 'The resulting encrypted+decrypted key does not match the original key object.')
