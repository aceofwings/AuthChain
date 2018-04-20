import unittest
from authchain.components import services
from authchain.components import crypto
from cryptoconditions import Ed25519Sha256,ThresholdSha256


class TestServices(unittest.TestCase):

    def setUp(self):
        self.service = crypto.generate_key_pair()
        self.alice = crypto.generate_key_pair()
        self.bob = crypto.generate_key_pair()
        self.singleMessage = services.generate_service(self.service.public_key, [self.alice.public_key])
        self.multimessage = services.generate_service(self.service.public_key, [self.alice.public_key,self.bob.public_key])


    def tearDown(self):
        pass

    def test_generateUnsignedTxSingleOwner(self):
        message = services.generate_service(self.service.public_key, [self.alice.public_key])

    def test_generateUnsignedTxMultiOwner(self):
        message = services.generate_service(self.service.public_key, [self.alice.public_key,self.bob.public_key])

    def test_generateSignedTx(self):
        signedmessage = services.sign_service(self.singleMessage, [self.alice.private_key])

    def test_generateMultiSignedTx(self):
        signedmessage = services.sign_service(self.multimessage, [self.alice.private_key, self.bob.private_key])

    def test_validate_service(self):
        signedmessage = services.sign_service(self.singleMessage, [self.alice.private_key])
        services.verifyService(signedmessage)
