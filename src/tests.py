import unittest
import hashlib
from SHA3 import sha3_n
from main import generate_random_message


class TestSHA(unittest.TestCase):

    def test_sha3_224(self):
        msg = generate_random_message(100)
        self.assertEqual(sha3_n(msg, 224), hashlib.sha3_224(msg.encode('utf-8')).hexdigest())

    def test_sha3_256(self):
        msg = generate_random_message(100)
        self.assertEqual(sha3_n(msg, 256), hashlib.sha3_256(msg.encode('utf-8')).hexdigest())

    def test_sha3_384(self):
        msg = generate_random_message(100)
        self.assertEqual(sha3_n(msg, 384), hashlib.sha3_384(msg.encode('utf-8')).hexdigest())

    def test_sha3_512(self):
        msg = generate_random_message(100)
        self.assertEqual(sha3_n(msg, 512), hashlib.sha3_512(msg.encode('utf-8')).hexdigest())


