import unittest
from authchain.components import services
from authchain.components import crypto
from cryptoconditions import Ed25519Sha256,ThresholdSha256


class TestServices(unittest.TestCase):

    def setUp(self):
        self.service = crypto.generate_key_pair()
        self.alice = crypto.generate_key_pair()
        self.bob = crypto.generate_key_pair()


    def tearDown(self):
        pass

    def test_generateUnsignedTxSingleOwner(self):
        message = services.generate_service(self.service.public_key, [self.alice.public_key])
        print(message)

    def test_generateUnsignedTxSingleOwner(self):
        message = services.generate_service(self.service.public_key, [self.alice.public_key,self.bob.public_key])
        print(message)
